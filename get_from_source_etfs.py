import requests
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
# from . import HashTable, FundsDB

get_from_source_etfs = Flask(__name__)
get_from_source_etfs.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///etfsdb.db"
get_from_source_etfs.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(get_from_source_etfs)
get_from_source_etfs.app_context().push()

class EtfsDB(db.Model):
    __tablename__ = 'EtfsDB'
    sn = db.Column(db.Integer(), primary_key=True, nullable=False)    
    isin = db.Column(db.String(),  nullable=True)
    SecId = db.Column(db.String(), nullable=True)
    Name = db.Column(db.String(), nullable=True)
    TenforeId = db.Column(db.Integer(), nullable=True)
    ExchangeId = db.Column(db.String(), nullable = True)
    ExchangeCode = db.Column(db.String(), nullable = True)
    holdingTypeId = db.Column(db.Integer(), nullable=True)
    sedol = db.Column(db.String(), nullable=True)
    # CustomIsClosed = db.Column(db.Boolean(), nullable=True)
    CustomIsFavourite = db.Column(db.Boolean(), nullable=True)
    CustomIsRecommended = db.Column(db.Boolean(), nullable=True)
    QR_MonthDate = db.Column(db.String(), nullable=True)
    Currency = db.Column(db.String(), nullable=True)
    LegalName = db.Column(db.String(), nullable=True)
    Yield_M12 = db.Column(db.String(), nullable=True)
    OngoingCostEstimated = db.Column(db.String(), nullable=True)
    # CustomCategoryId3Name = db.Column(db.String(), nullable=True)
    StarRatingM255 = db.Column(db.Integer(), nullable=True)
    QR_GBRReturnM12_5 = db.Column(db.String(), nullable=True)
    QR_GBRReturnM12_4 = db.Column(db.String(), nullable=True)
    QR_GBRReturnM12_3 = db.Column(db.String(), nullable=True)
    QR_GBRReturnM12_2 = db.Column(db.String(), nullable=True)
    QR_GBRReturnM12_1 = db.Column(db.String(), nullable=True)
    CustomMinimumPurchaseAmount = db.Column(db.Integer(), nullable=True)
    # CustomAdditionalBuyFee = db.Column(db.Integer(), nullable=True)
    # CustomSellFee = db.Column(db.Integer(), nullable=True)
    TransactionFeeEstimated = db.Column(db.String(), nullable=True)
    GBRReturnM0 = db.Column(db.String(), nullable=True)
    GBRReturnM12 = db.Column(db.String(), nullable=True)
    GBRReturnM36 = db.Column(db.String(), nullable=True)
    GBRReturnM60 = db.Column(db.String(), nullable=True)
    GBRReturnM120 = db.Column(db.String(), nullable=True)
    TrackRecordExtension = db.Column(db.Boolean(), nullable=True)
    def __repr__(self):
        return f"<Fund ISIN - {self.isin}, Fund Name - {self.Name}>"


class HashTable:
    def __init__(self):
        self.table = {}

    def insert(self, dictionary):
        isin = dictionary['isin']
        self.table[isin] = dictionary
        # self.table = dictionary

    def get(self, isin):
        return self.table.get(isin)
    
    def getAll(self):
        return self.table


@get_from_source_etfs.route('/', methods=['GET'])
def home():
    data = {}
    endpoints = {}
    
    data['Details'] = 'This is Exchange Traded Funds APi. You can use this api to get information about the ETFs in our database.'
    
    endpoints['/'] = 'Information Page'
    endpoints['/data_load_etfs'] = 'Use this endpoint to feed data into the database in bulk. Ensure that the database is clear or you might get database error in case primary key clash.'
    endpoints['/isin/<isin>'] = 'Use this endpoint to get details of any particulat isin. Example /isin/GB00B2PB2C75 will provide details of GB00B2PB2C75. If the mentioned isin is not present in database then you would see error.'
    data['routes'] = endpoints
    
    return data

@get_from_source_etfs.route('/data_load_etfs', methods=['GET'])
def get_data():
    # Make a request to the external API
    
    source_url = "https://lt.morningstar.com/api/rest.svc/9vehuxllxs/security/screener?page=1&pageSize=5000&sortOrder=LegalName%20asc&outputType=json&version=1&languageId=en-GB&currencyId=GBP&universeIds=ETEXG%24XLON_3518%7CETALL%24%24ALL_3518&securityDataPoints=SecId%7CName%7CTenforeId%7CholdingTypeId%7Cisin%7Csedol%7CQR_MonthDate%7CCustomIsFavourite%7CCustomIsRecommended%7CExchangeId%7CExchangeCode%7CCurrency%7CLegalName%7CYield_M12%7COngoingCostEstimated%7CStarRatingM255%7CCustomCategoryId3Name%7CCollectedSRRI%7CQR_GBRReturnM12_5%7CQR_GBRReturnM12_4%7CQR_GBRReturnM12_3%7CQR_GBRReturnM12_2%7CQR_GBRReturnM12_1%7CCustomMinimumPurchaseAmount%7CTransactionFeeEstimated%7CPerformanceFee%7CGBRReturnM0%7CGBRReturnM12%7CGBRReturnM36%7CGBRReturnM60%7CGBRReturnM120%7CTrackRecordExtension&filters=&term=&subUniverseId=ETFEI" 
    response = requests.get(source_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        json_data = response.json()
        x = json_data['rows']
        fundshash = HashTable()
        for dictionary in x:
            fundshash.insert(dictionary)       

    else:
        # If the request was not successful, return an error message
        return jsonify({'error': 'Failed to fetch data from the API'}), 500
    
    # put it in the database. 
    

    sn = 1
    error_list = []
    for item in fundshash.table:
        try:
            isin = fundshash.table[item]['isin']
            try:
                sedol = fundshash.table[item]['sedol']
            except Exception as e:
                sedol = 'NA'
            SecId = fundshash.table[item]['SecId']
            Name = fundshash.table[item]['Name']
            try:
                TenforeId = fundshash.table[item]['TenforeId']
            except Exception as e:
                TenforeId = 'NA'
            holdingTypeId = fundshash.table[item]['holdingTypeId']
            # CustomIsClosed = fundshash.table[item]['CustomIsClosed']
            CustomIsFavourite = fundshash.table[item]['CustomIsFavourite']
            CustomIsRecommended = fundshash.table[item]['CustomIsRecommended']
            QR_MonthDate = fundshash.table[item]['QR_MonthDate']
            Currency = fundshash.table[item]['Currency']
            LegalName = fundshash.table[item]['LegalName']
            try:
                Yield_M12 = fundshash.table[item]['Yield_M12']
            except Exception as e:
                Yield_M12 = 'NA'
            OngoingCostEstimated = fundshash.table[item]['OngoingCostEstimated']
            # try:
            #     CustomCategoryId3Name = fundshash.table[item]['CustomCategoryId3Name']
            # except Exception as e:
            #     CustomCategoryId3Name = 'NA'
            try:
                StarRatingM255 = fundshash.table[item]['StarRatingM255']
            except Exception as e:
                StarRatingM255 = 'NA'
            try:
                QR_GBRReturnM12_5 = fundshash.table[item]['QR_GBRReturnM12_5']
            except Exception as e:
                QR_GBRReturnM12_5 = 'NA'
            try:
                QR_GBRReturnM12_4 = fundshash.table[item]['QR_GBRReturnM12_4']
            except Exception as e:
                QR_GBRReturnM12_4 = 'NA'
            try:
                QR_GBRReturnM12_3 = fundshash.table[item]['QR_GBRReturnM12_3']
            except Exception as e:
                QR_GBRReturnM12_3 = 'NA'
            QR_GBRReturnM12_2 = fundshash.table[item]['QR_GBRReturnM12_2']
            QR_GBRReturnM12_1 = fundshash.table[item]['QR_GBRReturnM12_1']
            try:
                CustomMinimumPurchaseAmount = fundshash.table[item]['CustomMinimumPurchaseAmount']
            except Exception as e:
                CustomMinimumPurchaseAmount = 'NA'
            # CustomAdditionalBuyFee = fundshash.table[item]['CustomAdditionalBuyFee']
            # CustomSellFee = fundshash.table[item]['CustomSellFee']
            TransactionFeeEstimated = fundshash.table[item]['TransactionFeeEstimated']
            try:
                GBRReturnM0 = fundshash.table[item]['GBRReturnM0']
            except Exception as e:
                GBRReturnM0 = 'NA'
            try:
                GBRReturnM12 = fundshash.table[item]['GBRReturnM12']
            except Exception as e:
                GBRReturnM12 = 'NA'
            try:
                GBRReturnM36 = fundshash.table[item]['GBRReturnM36']
            except Exception as e:
                GBRReturnM36 = 'NA'
            try:
                GBRReturnM60 = fundshash.table[item]['GBRReturnM60']
            except Exception as e:
                GBRReturnM60 = 'NA'
            try:
                GBRReturnM120 = fundshash.table[item]['GBRReturnM120']
            except Exception as e:
                GBRReturnM120 = 'NA'
            TrackRecordExtension = fundshash.table[item]['TrackRecordExtension']
            print('isin- ', isin)
            print('TrackRecordExtension-' , TrackRecordExtension)
            
        
            fund = EtfsDB(sn = sn, isin = isin, sedol = sedol, SecId = SecId, Name = Name, TenforeId = TenforeId, holdingTypeId = holdingTypeId, CustomIsFavourite = CustomIsFavourite, CustomIsRecommended = CustomIsRecommended, QR_MonthDate = QR_MonthDate, Currency = Currency, LegalName = LegalName, Yield_M12 = Yield_M12, OngoingCostEstimated = OngoingCostEstimated, StarRatingM255 = StarRatingM255, QR_GBRReturnM12_5 = QR_GBRReturnM12_5, QR_GBRReturnM12_4 = QR_GBRReturnM12_4, QR_GBRReturnM12_3 = QR_GBRReturnM12_3, QR_GBRReturnM12_2 = QR_GBRReturnM12_2, QR_GBRReturnM12_1 = QR_GBRReturnM12_1, CustomMinimumPurchaseAmount = CustomMinimumPurchaseAmount,  TransactionFeeEstimated = TransactionFeeEstimated, GBRReturnM0 = GBRReturnM0, GBRReturnM12 = GBRReturnM12, GBRReturnM36 = GBRReturnM36, GBRReturnM60 = GBRReturnM60, GBRReturnM120 = GBRReturnM120, TrackRecordExtension = TrackRecordExtension  )
            db.session.add(fund)
            print(fund)
            db.session.commit()
            sn = sn +1          
            
        except Exception as e:
            if e not in error_list:
                error_list.append(e)
    print(error_list)
    return fundshash.table


@get_from_source_etfs.route('/isin/<isin>', methods=['GET'])
def get_isin(isin):
    try:
        fund = EtfsDB.query.filter_by(isin=isin).first()
        print(type(fund))
        print(fund)
        data = {}

        i = 0
        for name, value, in vars(fund).items():
            if i == 0:
                pass
            else:         
                data[name] = value
            i = i+1
        return data
    except Exception as e:
        txt = 'Mentioned ISIN not prsent in db. Please check!!! ' + isin
        print('Exception Occured:-', e)
        print('Mentioned ISIN not prsent in db')
        return txt

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    get_from_source_etfs.run(debug=True, host='0.0.0.0', port=port)
