from sqlalchemy import (create_engine,
                        Column,
                        Integer,
                        String,
                        ForeignKey,
                        Enum,
                        Boolean)
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

engine = create_engine('sqlite:///atividades.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class StatusAtividade(str, enum.Enum):
    pendente = 'pendente'
    concluido = 'concluído'

    @classmethod
    def validar_status(cls, status):
        if status not in [cls.pendente, cls.concluido]:
            return False
        else:
            return True


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


class Pessoas(TabelaBase):
    __tablename__ = 'pessoas'
    nome = Column(String(40), index=True)
    idade = Column(Integer)


class Atividades(TabelaBase):
    __tablename__ = 'atividades'
    nome = Column(String(80))
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))
    status = Column(Enum(StatusAtividade), default=StatusAtividade.pendente)
    pessoa = relationship('Pessoas')


class Usuarios(TabelaBase):
    __tablename__ = 'usuarios'
    login = Column(String(20), unique=True)
    senha = Column(String(20))
    ativo = Column(Boolean, default=True)

    def __repr__(self):
        return f'{self.login}'


def init_db():
    Base.metadata.create_all(bind=engine, tables=[Pessoas.__table__,
                                                  Atividades.__table__,
                                                  Usuarios.__table__])


if __name__ == '__main__':
    init_db()
