# scrapy crawl tcg -o pokemon.csv
import scrapy

class TcgSpider(scrapy.Spider):
    name = "tcg"

    async def start(self):
        urls = [
            'https://limitlesstcg.com/cards/PFL',
            'https://limitlesstcg.com/cards/MEG',
            'https://limitlesstcg.com/cards/BLK',
            'https://limitlesstcg.com/cards/WHT',
            'https://limitlesstcg.com/cards/DRI',
            'https://limitlesstcg.com/cards/JTG',
            'https://limitlesstcg.com/cards/PRE',
            'https://limitlesstcg.com/cards/SSP',
            'https://limitlesstcg.com/cards/SCR',
            'https://limitlesstcg.com/cards/SFA',
            'https://limitlesstcg.com/cards/TWM',
            'https://limitlesstcg.com/cards/TEF',
            'https://limitlesstcg.com/cards/PAF',
            'https://limitlesstcg.com/cards/PAR',
            'https://limitlesstcg.com/cards/MEW',
            'https://limitlesstcg.com/cards/OBF',
            'https://limitlesstcg.com/cards/PAL',
            'https://limitlesstcg.com/cards/SVI'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_set)

    # Get the URL for each card in each set
    def parse_set(self, response):
        index = response.css('div.card-search-grid a::attr(href)').getall()
        index_set = set(index)
        for idx in index_set:
            url = response.urljoin(idx)
            yield scrapy.Request(url=url, callback=self.get_card_attributes)

    # Get attributes for each card
    def get_card_attributes(self, response):

        card_title_parts = response.css('p.card-text-title::text').getall()
        card_title = ' '.join([part.strip() for part in card_title_parts if part.strip()])
        card_type_elt = response.css('p.card-text-type::text').get()

        # Get card type
        card_type = None
        if card_type_elt and 'Pokémon' in card_type_elt:
            if card_title:
                split_title = [part.strip() for part in card_title.split('-')]
                if len(split_title) >= 3:
                    card_type = split_title[1]
        else:
            card_type = 'Trainer'

        # Get hp (for pokemon)
        hp = "None"
        if card_title and card_type and card_type != 'Trainer':
            split_title = [part.strip() for part in card_title.split('-')]
            if len(split_title) >= 3:
                hp = split_title[-1].replace('HP', '').strip()

        # Get price
        price_text = response.css('span.card-price.usd::text').get()
        price = None
        if price_text:
            price = price_text.strip().replace('$', '')

        # Get ability name (if exists)
        ability_text = response.css('p.card-text-ability-info::text').getall()
        ability_name = "None"
        if len(ability_text) >= 2:
            ability_name = ' '.join(ability_text[1].split()).replace('Ability:', '').strip()
        elif len(ability_text) == 1:
            text = ' '.join(ability_text[0].split()).replace('Ability:', '').strip()
            if text and text != 'Ability:':
                ability_name = text

        # Get the card rarity
        rarity_text = response.css('div.prints-current-details span:nth-child(2)::text').get()
        rarity = "Unspecified"
        if rarity_text and '·' in rarity_text:
            rarity = rarity_text.split('·')[-1].strip()

        # Get the card's set number
        set_number = None
        if rarity_text:
            if '·' in rarity_text:
                set_number = rarity_text.split('·')[0].strip().replace('#', '')
            else:
                set_number = rarity_text.strip().replace('#', '')

        yield {
            'url': response.url,
            'image': response.css('div.card-image img::attr(src)').get(),
            'name': response.css('span.card-text-name a::text').get().strip(),
            'type': card_type,
            'rarity': rarity,
            'artist': response.css('div.card-text-artist a::text').get().strip(),
            'set': response.css('div.prints-current-details span.text-lg::text').get().strip(),
            'price': price,
            'ability': ability_name,
            'HP': hp,
            'set_number': set_number
        }
