# Opetussovellus

## Tarkoitus
Sovelluksen tarkoituksena on toimia alustana verkkokurssien järjestämiselle. Alustalla oleviin verkkokursseihin sisältyy kyseisen kurssin kuvista ja tekstistä koostuva opetusmateriaali sekä opiskelijan oppimista mittaavat ja oppilaiden oppimisesta dataa keräävät testit. Kurssin testit voivat olla monivalintatestejä tai kirjallisia testejä. 

Käyttäjän tulee kirjautua sisään ennen kun tämä pääsee käyttämään sovellusta. Jos olemassa olevaa tunnusta ei ole, käyttäjä voi luoda uuden käyttäjätunnuksen. Sovelluksessa on kaksi käyttäjäroolia jotka määrittävät käyttäjälle mahdolliset toiminnot. "Opettaja"-roolin omaava käyttäjä voi lisätä sovellukseen verkkokurssin sekä lisätä, poistaa tai muokata itse luomiensa kurssien sisältöä. Hän voi myös nähdä omalle kurssilleen liittyneet oppilaat ja sen miten oppilaat ovat suoriutuneet kyseisen kurssin oppimista mittaavista testeistä. "Oppilas"-roolin omaava näkee alustalle luodut verkkokurssit sekä niiden sisällön. Lisäksi hän voi vastata kursseihin sisältyviin testeihin. 

## Käyttöohjeet
Kloonaa repositio ja luo kloonaamaasi kansioon .env-tiedosto. Tiedostosta tulee löytyä seuraavat  määrittelyt:

DATABASE_URL=postgresql:///(käyttäjänimi) jossa käyttäjänimi tulee korvata omalla käyttäjänimelläsi sekä
SECRET_KEY=(itse generoimasi salainen avain)

Tarvittavien riippuvuuksien ja virtuaaliympäristön asentaminen onnistuu seuraavin komennoin:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r ./requirements.txt
```
ja skeemat tulee asentaa komennolla 
```
psql < tables.sql
```
Sovellus käynnistetään seuraavalla komennolla
```
flask run
```
Tämän jälkeen käyttö luonnistuu sovelluksen antamien ohjeiden avulla.
Huomaa että sovellus ei välttämättä toimi kunnolla jos JavaScript on kytketty pois päältä selainasetuksissa.