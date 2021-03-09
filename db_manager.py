from pathlib import Path

import pandas as pd
from sqlalchemy import literal

from orm import Supplier, Country, Customer, DataAccessLayer, Product, Category, PriceTable


class DBManager:

    def __init__(self):
        dal = DataAccessLayer()
        dal.conn_string = r"sqlite:///my_db.db"
        dal.echo = True
        dal.connect()
        self.session = dal.session_maker()

    def get_companies_names(self):
        return [i[0] for i in self.session.query(Supplier.name).all()]

    def get_countries_names(self):
        return [i[0] for i in self.session.query(Country.name).all()]

    def get_country_code(self, country):
        return self.session.query(Country.code).filter(Country.name == country).one()[0]

    def is_supplier_created(self):
        if len(self.session.query(Supplier).all()) > 0:
            return True
        else:
            return False

    def are_countries_populated(self):
        if len(self.get_countries_names()) == 0:
            return False
        else:
            return True

    def get_company(self):
        return self.session.query(Supplier).one()

    def get_customers_names(self):
        return [i[0] for i in self.session.query(Customer.name).all()]

    def get_customers_full_names(self):
        return [i[0] for i in self.session.query(Customer.full_name).all()]

    def get_customers_country_tin_codes(self):
        return [i[0] for i in self.session.query(Customer.country_tin).all()]

    def get_customer(self, customer_name):
        return self.session.query(Customer).filter(Customer.name == customer_name).one()

    def check_customer_names_constraint(self, name):
        q = self.session.query(Customer).filter(Customer.name == name)
        return self.session.query(literal(True)).filter(q.exists()).scalar()

    def check_customer_full_name_constraint(self, full_name):
        q = self.session.query(Customer).filter(Customer.full_name == full_name)
        return self.session.query(literal(True)).filter(q.exists()).scalar()

    def check_customer_country_tin_constraint(self, country, tin_code):
        q = self.session.query(Customer).filter(Customer.country == country, Customer.tin_code == tin_code)
        return self.session.query(literal(True)).filter(q.exists()).scalar()

    def get_all_products(self):
        return self.session.query(Product).all()

    def get_categories(self):
        return [i[0] for i in self.session.query(Category.name).all()]

    def category_exist(self, category_name):
        q = self.session.query(Category).filter(Category.name == category_name)
        return self.session.query(literal(True)).filter(q.exists()).scalar()

    def get_price_table(self, customer_id):
        return self.session.query(PriceTable).filter(PriceTable.customer_id == customer_id).all()

    def get_customer_id(self, *, customer_name=None, customer_full_name=None):
        q = self.session.query(Customer.id)
        if customer_name is not None:
            q = q.filter(Customer.name == customer_name)
        if customer_full_name is not None:
            q = q.filter(Customer.full_name == customer_full_name)
        return q.one()[0]

    def get_all_products_names(self):
        return [i[0] for i in self.session.query(Product.name).all()]


db_manager = DBManager()


def populate_countries():
    #  use to populate DB with countries
    df = pd.read_csv(Path().absolute().joinpath('Countries_table.csv'))
    df = df[~pd.isna(df['Alpha-2 code'])]
    df['Country'] = df['Country'].str.replace('\(.*\)', '').str.replace('\[.*\]', '').str.strip()
    items = []
    for _, row in df.iterrows():
        items.append(Country(name=row['Country'], code=row['Alpha-2 code']))
    db_manager.session.add_all(items)
    db_manager.session.commit()