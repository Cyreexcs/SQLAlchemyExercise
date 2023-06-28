from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapped_column
from sqlalchemy import *

engine = create_engine('sqlite:///SQLAlchemyDB.db', echo=True)


class Base(DeclarativeBase):
    pass

association_table=Table(
    'Association',
    Base.metadata,
    Column('personPID', ForeignKey('Persons.PID'), primary_key=True),
    Column('SchliessFachSID', ForeignKey('schliessfach.SID'), primary_key=True)
)

class Schliessfach(Base):
    __tablename__ = "schliessfach"
    SID : Mapped[int] = mapped_column(primary_key=True)
    ErstellungsDatum: Mapped[datetime.date] = mapped_column()
    eigentumerName: Mapped[str] = mapped_column(ForeignKey("Eigentumern.unternehmensName"), nullable=True)
    eigentumer: Mapped["Eigentumer"] = relationship(back_populates="schliessFachList")
    persons = relationship('Person',secondary=association_table,back_populates='schliessFachList')

    def __init__(self,  ErstellungsDatum):
        self.ErstellungsDatum = ErstellungsDatum

    def __repr__(self):
        print(self.SID)

class Person(Base):
    __tablename__ = "Persons"
    PID: Mapped[int] = mapped_column(primary_key=True)
    vorname: Mapped[int] = mapped_column()
    nachname: Mapped[int] = mapped_column()
    schliessFachList = relationship('Schliessfach',secondary=association_table,back_populates='persons')

    def __init__(self,vorname, nachname):
        self.nachname = nachname
        self.vorname = vorname

class Eigentumer(Base):
    __tablename__ = "Eigentumern"
    unternehmensName: Mapped[str] = mapped_column(primary_key=True)
    leanderCode : Mapped[str] = mapped_column()
    schliessFachList: Mapped[list[Schliessfach]] = relationship(back_populates="eigentumer")

    def __init__(self, unternehmensName, leandercode):
        self.unternehmensName = unternehmensName
        self.leanderCode = leandercode

Base.metadata.create_all(engine)

session = sessionmaker()(bind = engine)
def filldb(session):
    Person1 = Person(1, 2)
    Person2 = Person(3, 4)
    Person3 = Person(4, 5)
    Eigentumer1 = Eigentumer("BlackRock", "9001")
    Eigentumer2 = Eigentumer("Allianz", "2131")
    Schliessfach1 = Schliessfach(datetime.date.today())
    Schliessfach2 = Schliessfach(datetime.date.today())
    Schliessfach3 = Schliessfach(datetime.date.today())
    Schliessfach4 = Schliessfach(datetime.date.today())

    Schliessfach1.persons.append(Person2)
    Schliessfach4.persons.append(Person1)
    Schliessfach4.persons.append(Person2)
    Schliessfach2.persons.append(Person3)
    Schliessfach3.persons.append(Person3)

    Eigentumer1.schliessFachList.append(Schliessfach1)
    Eigentumer2.schliessFachList.append(Schliessfach2)

    session.add_all([Eigentumer2, Eigentumer1,Schliessfach1, Schliessfach2, Schliessfach3, Schliessfach4, Person1, Person2, Person3 ])

    session.commit()

filldb(session)
#ausgabe alle Eigentumer
looping = True
while (looping):
    print()
    print("1: Ausgabe aller Eigentuemer")
    print("2: Ausgabe aller schliessfaecher")
    print("3: Ausgabe aller Personen")
    print("4: Ausgabe aller Schließfaecher eines Berechtigten")
    print("5: Exit Please")

    input_ =  input("Choose: ")
    if input_ == "1" :
        EigentumerList = session.query(Eigentumer).all()
        for obj in EigentumerList:
            print("Name: " + obj.unternehmensName + " | Code: " + obj.leanderCode)

    elif input_ == "2":
        EigentumerName = input("Give Eigentumer Name")
        eigentumerObj = session.get(Eigentumer, EigentumerName)
        for obj in eigentumerObj.schliessFachList:
            obj.__repr__()

    elif input_ == "3":
        PersonList = session.query(Person).all()
        for obj_ in PersonList:
            print("PID: " + str(obj_.PID) + " | Nachname: " + str(obj_.nachname) + " | Vorname: " + str(obj_.vorname))

    elif input_ == "4":
        PersonId = input("Give Persons ID")
        personObj = session.get(Person, PersonId)
        for obj in personObj.schliessFachList:
            obj.__repr__()

    elif input_ == "5":
        looping = False
    else:
        print("Wrong Input, Choose Again  !")
