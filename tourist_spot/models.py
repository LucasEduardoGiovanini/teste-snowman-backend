from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class GerenciadorPerfilUsuario(BaseUserManager):
    def criar_usuario(self, email, nome, senha):
        email = self.normalize_email(email)
        usuario = self.model(email, nome)

        usuario.set_password(senha)  # encripta
        usuario.save(using=self._db)
        return usuario

    def criar_superusuario(self, email, nome, senha):
        super_usuario = self.criar_usuario(email, nome, senha)

        super_usuario.is_superuser = True
        super_usuario.is_staff = True
        super_usuario.save(using=self._db)
        return super_usuario


class PerfilUsuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    nome = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = GerenciadorPerfilUsuario()

    def recupera_nome(self):
        return self.nome

    def __str__(self):
        return self.email


class Categoria(models.Model):
    nome = models.CharField(max_length=50)


class PontoTuristico(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField(max_length=40)
    longitude = models.FloatField(max_length=40)

    categoria = models.ForeignKey(Categoria,
                                  on_delete=models.CASCADE,
                                  )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class GerenciadorPontoTuristico():
    def consulta_categoria(self, categoria: str):
        categoria_existente = PontoTuristico().objects.get(categoria=categoria.upper())
        return categoria_existente if categoria_existente else False

    def consulta_ponto_turistico(self, ponto_turistico: PontoTuristico.nome):
        ponto_turistico = PontoTuristico().objects.get(name=ponto_turistico.upper())
        return ponto_turistico if ponto_turistico else False
