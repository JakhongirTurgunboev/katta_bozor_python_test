import requests
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Offer


# Test fetching data from the API
def test_fetch_data():
    api_url = 'https://www.kattabozor.uz/hh/test/api/v1/offers'
    response = requests.get(api_url)
    assert response.status_code == 200
    data = response.json()
    assert 'offers' in data


# Test saving data to the database
def test_save_to_database():
    engine = create_engine('sqlite:///offers.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    test_offer = None

    # Check if the test offer already exists in the database
    existing_offer = session.query(Offer).filter_by(id=999).first()

    if existing_offer:
        print("Test offer already exists in the database. Skipping insertion.")
    else:
        # Insert the test offer
        test_offer = Offer(
            id=999,
            name="Test Offer",
            brand="Test Brand",
            category="Test Category",
            merchant="Test Merchant",
            attributes=[],
            image_url="https://test_image_url.com"
        )
        session.add(test_offer)
        session.commit()

    # Retrieve the test offer from the database
    retrieved_offer = session.query(Offer).filter_by(id=999).first()

    assert retrieved_offer is not None
    assert retrieved_offer.name == "Test Offer"
    assert retrieved_offer.brand == "Test Brand"

    # Clean up after the test
    if test_offer is not None:
        session.delete(test_offer)
    session.commit()

    session.close()


if __name__ == '__main__':
    pytest.main(['-v', 'test_script.py'])

