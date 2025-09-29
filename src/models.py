from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, Date, BigInteger
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_sub: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favoritos = relationship("Favorito", back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "fecha_sub": self.fecha_sub,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }


class Planeta(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    clima: Mapped[str] = mapped_column(String(20))
    terreno: Mapped[str] = mapped_column(String(120))
    poblacion: Mapped[int] = mapped_column(BigInteger)

    personajes = relationship("Personaje", back_populates="planeta")
    favoritos = relationship("Favorito", back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno,
            "poblacion": self.poblacion,
            # do not serialize the password, its a security breach
        }


class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    genero: Mapped[str] = mapped_column(String(20))
    altura: Mapped[int] = mapped_column(Integer, nullable=False)
    color_ojos: Mapped[str] = mapped_column(String(20))
    color_pelo: Mapped[str] = mapped_column(String(20))
    planeta_id: Mapped[int] = mapped_column(Integer, ForeignKey("planeta.id"))

    planeta = relationship("Planeta", back_populates="personajes")
    favoritos = relationship("Favorito", back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "altura": self.altura,
            "color_ojos": self.color_ojos,
            "color_pelo": self.color_pelo,
            "planeta_id": self.planeta_id,
            # do not serialize the password, its a security breach
        }


class Favorito(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False)
    planeta_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("planeta.id"), nullable=True)
    personaje_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("personaje.id"), nullable=True)
    fecha_guardado: Mapped[date] = mapped_column(Date, default=date.today)

    usuario = relationship("User", back_populates="favoritos")
    planeta = relationship("Planeta", back_populates="favoritos")
    personaje = relationship("Personaje", back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "planeta_id": self.planeta_id,
            "personaje_id": self.personaje_id,
            "fecha_guardado": self.fecha_guardado,
        }
