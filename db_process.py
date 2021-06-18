
from sqlalchemy.sql.sqltypes import DateTime, Float

from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine('postgresql+psycopg2://postgres:asd123@localhost:5432/postgres')
Base = declarative_base()

Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()


class Device(Base):
    __tablename__='Data'
    id = Column(Integer,primary_key = True,unique=True,autoincrement=True)
    deviceId = Column(String)
    system_ip = Column(String)
    status = Column(String)
    board_serial = Column(String)
    device_type = Column(String)
    uuid = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    state = Column(String)
    site_id = Column(String)
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

class AlarmByHours(Base):
    __tablename__='AlarmHours'
    id = Column(Integer,primary_key = True,unique=True,autoincrement=True)
    system_ip = Column(String)
    site_id = Column(String)
    message = Column(String)
    severity = Column(String)
    receive_time = Column(String)
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

class AlarmEvent(Base):
    __tablename__='AlarmEvent'
    id = Column(Integer,primary_key = True,unique=True,autoincrement=True)
    eventname = Column(String)
    severity_level = Column(String)
    system_ip = Column(String)
    entry_time = Column(String)
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def addData(deviceId, system_ip, status, board_serial, device_type, uuid,latitude,longitude,state, site_id):
    with session_scope() as s:
        std=Device(
            deviceId=deviceId,
            system_ip=system_ip,
            status=status,
            board_serial=board_serial,
            device_type=device_type,
            uuid=uuid,
            latitude=latitude,
            longitude=longitude,
            state=state,
            site_id=site_id
        )
        s.add(std)


def addAlarmData(system_ip, message, severity,receive_time):
    with session_scope() as s:
        std=AlarmByHours(
            system_ip=system_ip,
            message=message,
            severity=severity,
            receive_time=receive_time
        )
        s.add(std)

def addAlarmEvent(eventname, severity_level, system_ip, entry_time):
    with session_scope() as s:
        std=AlarmEvent(
            eventname=eventname,
            severity_level=severity_level,
            system_ip=system_ip,
            entry_time=entry_time
        )
        s.add(std)


def getDevice():
    with session_scope() as s:
        device_list=s.query(Device).all()
        
        for elem in device_list:
            print(elem.id,elem.deviceId, elem.system_ip, elem.status, elem.board_serial, elem.device_type, elem.uuid, elem.latitude, elem.longitude, elem.state, elem.site_id)

def getAlarmData():
    with session_scope() as s:
        device_list=s.query(AlarmByHours).all()
        
        for elem in device_list:
            print(elem.system_ip, elem.message, elem.severity, elem.receive_time)

def getAlarmEvent(system_ip):
    with session_scope() as s:
        device_list=s.query(AlarmEvent).filter(AlarmEvent.system_ip==(str(system_ip))).all()
        
        for elem in device_list:
            #if elem.system_ip == str(system_ip):
            print(elem.eventname, elem.severity_level, elem.system_ip, elem.entry_time)


def getAll(system_ip):
    with session_scope() as s:
        device_list=s.query(AlarmEvent, AlarmByHours).join(AlarmByHours, AlarmByHours.system_ip == AlarmEvent.system_ip).filter(AlarmByHours.system_ip == str(system_ip)).all()
        #print(device_list)
        for event, hour in device_list:
            #if elem.system_ip == str(system_ip):
            print(event.eventname, event.severity_level,  event.system_ip, hour.severity, hour.system_ip)


class CoinDB(Base):
    __tablename__='CoinDB'
    id = Column(Integer,primary_key = True,autoincrement=True,unique=True)
    coin_id=Column(Integer)
    name = Column(String)
    symbol = Column(String)
    slug = Column(String)
    p = Column(Float)
    v = Column(Float)
    date = Column(DateTime)
    #timestamp = Column(DateTime)
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def addCoinData(id, name, symbol, slug, p, v,date,timestamp):
    with session_scope() as s:
        std=CoinDB(
            coin_id = str(id),
            name = name,
            symbol = symbol,
            slug = slug,
            p = p,
            v = v,
            date = date
            #timestamp = timestamp
        )
        s.add(std)


def getCoinData():
    with session_scope() as s:
        device_list=s.query(CoinDB).all()
        
        for elem in device_list:
            print(elem.coin_id, elem.name, elem.symbol, elem.slug, elem.p, elem.v, elem.date, elem.timestamp)
