import asyncpg
import asyncio

PERSONAL_TABLE = """
    CREATE TYPE Rolle AS ENUM ('ADMIN', 'PERSONAL');
    CREATE TABLE Personen(
        id SERIAL4 PRIMARY KEY,
        rolle Rolle NOT NULL
    );
"""

GEBAEUDE_TABLE = """
    CREATE TABLE Gebaeude(
        id SERIAL4 PRIMARY KEY,
        name varchar(100) NOT NULL
    );
"""

STOCKWERKE_TABLE = """
    CREATE TABLE Stockwerke(
        id SERIAL4 PRIMARY KEY,
        idGebaeude int4 NOT NULL,
        name varchar(100) NOT NULL,        
        FOREIGN KEY (idGebaeude) REFERENCES Gebaeude(id)
    );
"""

RAEUME_TABLE = """
    CREATE TABLE Raeume(
        id SERIAL4 PRIMARY KEY,
        idStockwerk int4 NOT NULL,
        name varchar(100) NOT NULL,
        FOREIGN KEY (idStockwerk) REFERENCES Stockwerke(id)
    );
"""

SENSOREN_TABLE = """
    CREATE TABLE Sensoren(
        dev_eui VARCHAR(16) PRIMARY KEY,
        idRaum int4 NOT NULL,
        name VARCHAR(100) NOT NULL,
        FOREIGN KEY (idRaum) REFERENCES Raeume(id)
    );
"""

SENSOR_WERTE_TABLE = """
    CREATE TABLE SensorenWerte(
        id SERIAL4 PRIMARY KEY,
        dev_euiSensor VARCHAR(16) NOT NULL,
        rohWert VARCHAR NOT NULL,
        dekodiertJSON TEXT NOT NULL,
        erhalten timestamp,
        FOREIGN KEY (dev_euiSensor) REFERENCES Sensoren(dev_eui)
    );
"""

MELDUNGEN_TABLE = """
    CREATE TYPE MeldungsArt AS ENUM('AUTO', 'PERSONAL');
    CREATE TABLE Meldungen(
        id SERIAL4 PRIMARY KEY,
        dev_euiSensor VARCHAR(16),
        idRaum int4 NOT NULL,
        idPerson int4,
        art MeldungsArt NOT NULL,
        datum timestamp NOT NULL,
        bearbeitet boolean DEFAULT false,
        beschreibung TEXT NOT NULL
    );
"""

async def create_tables():
    connection = await asyncpg.connect(host='localhost', database='ipa', user='postgres', password='postgres')
    await connection.execute(GEBAEUDE_TABLE)
    await connection.execute(STOCKWERKE_TABLE)
    await connection.execute(RAEUME_TABLE)
    await connection.execute(PERSONAL_TABLE)
    await connection.execute(SENSOREN_TABLE)
    await connection.execute(SENSOR_WERTE_TABLE)
    await connection.execute(MELDUNGEN_TABLE)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(create_tables())
