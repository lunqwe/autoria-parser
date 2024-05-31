from .scrapper import Scrapper
from database.models import Card
from database.config import get_session


def check_for_unique(session, url):
    unique = session.query(Card).filter(Card.url == url).first()
    if unique:
        return True
    
    

def run():
    try:
        scrapper = Scrapper()
        scrapper.get_page_amount()
        session = next(get_session())
        for page_num in range(1, scrapper.page_amount):
            url = f'https://auto.ria.com/uk/car/used/?page={page_num}'
            page_cards = scrapper.get_cards_links(link=url)
            for url in page_cards:
                if "newauto" not in url and check_for_unique(url):
                    data = scrapper.get_card_data(link=url)
                    scrapper.logger.info(data)
                    card_obj = Card(**data)
                    session.add(card_obj)
                    session.commit()
        
    finally:
        scrapper.logger.info('Webscrapper has finished working')
        scrapper.driver.close()
        session.close()
            
    
            