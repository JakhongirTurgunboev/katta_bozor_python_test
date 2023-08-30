import requests
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the data model
Base = declarative_base()


class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    merchant = Column(String)
    attributes = Column(JSON)
    image_url = Column(String)


# API URL
api_url = 'https://www.kattabozor.uz/hh/test/api/v1/offers'

# Fetch data from the API
response = requests.get(api_url)
data = response.json()

# Create an SQLite database and establish a connection
engine = create_engine('sqlite:///offers.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Save data to the database
for offer_data in data['offers']:
    offer = session.query(Offer).filter_by(id=offer_data['id']).first()

    if offer:
        # Update existing offer
        offer.name = offer_data['name']
        offer.brand = offer_data['brand']
        offer.category = offer_data['category']
        offer.merchant = offer_data['merchant']
        offer.attributes = offer_data['attributes']
        offer.image_url = offer_data['image']['url']
    else:
        # Insert new offer
        offer = Offer(
            id=offer_data['id'],
            name=offer_data['name'],
            brand=offer_data['brand'],
            category=offer_data['category'],
            merchant=offer_data['merchant'],
            attributes=offer_data['attributes'],
            image_url=offer_data['image']['url']
        )
        session.add(offer)

session.commit()
session.close()

print("Data has been saved to the database.")
