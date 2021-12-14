from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///programadorapi.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class TabelaBase(Base):
    """
    Classe abstrata que sera herdada pelas tabelas
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f'{self.nome}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Programador(TabelaBase):
    __tablename__ = 'programador'

    nome = Column(String(40), index=True)
    idade = Column(Integer)
    email = Column(String(30))


class Habilidades(TabelaBase):
    __tablename__ = 'habilidades'
    nome = Column(String(60), index=True)


class ProgramadorHabilidade(TabelaBase):
    __tablename__ = 'programador_habilidade'
    programador = Column(Integer, ForeignKey('programador.id'))
    habilidade = Column(Integer, ForeignKey('habilidades.id'))


def init_db():
    Base.metadata.create_all(bind=engine, tables=[Programador.__table__,
                                                  Habilidades.__table__,
                                                  ProgramadorHabilidade.__table__])


if __name__ == '__main__':
    init_db()