# Opetussovellus

## Tarkoitus
Sovelluksen tarkoituksena on toimia alustana verkkokurssien järjestämiselle. Alustalla oleviin verkkokursseihin sisältyy kyseisen kurssin opetusmateriaali sekä opiskelijan oppimista mittaavat ja oppilaiden oppimisesta dataa keräävät testit. Kurssin testit voivat olla monivalintatestejä tai kirjallisia testejä. 

Käyttäjän tulee kirjautua sisään ennen kun tämä pääsee käyttämään sovellusta. Jos olemassa olevaa tunnusta ei ole, käyttäjä voi luoda uuden käyttäjätunnuksen. Sovellukselle tulee tällöin antaa käyttäjänimi joka ei ole valmiiksi käytössä, salasana sekä haluttu käyttäjärooli. Kun käyttäjä on kirjautunut sisään hän voi roolista riippumatta tarkastella käyttäjätiedoista omia käyttäjätietojaan, poistaa käyttäjätilin tai kirjautua ulos sovelluksesta.

Sovelluksessa on kaksi käyttäjäroolia ja rooli määrää käyttäjälle mahdolliset toiminnot. Opettaja-roolin omaava käyttäjä voi lisätä sovellukseen kursseja sekä lisätä, poistaa tai muokata itse luomiensa kurssien sisältöä. Opettaja näkee vain omat kurssinsa. Kurssisivulta opettaja näkee mitä tehtäviä oppilaat ovat ratkoneet oikein kyseiseltä kurssilta ja omista käyttäjätiedoista kuinka monta kurssitehtävää tehtäviä oikein ratkoneet oppilaat ovat tehneet kultakin opettajan tekemältä kurssilta.

Oppilas-roolin omaava näkee kaikki lisätyt kurssit sekä niiden materiaalit ja tehtävät. Oppilas voi vapaasti ratkoa kurssien tehtäviä ja oikein ratkaistut tehtävät näkyvät kyseisen kurssin sivulla. Käyttäjätiedoista oppilas näkee monta tehtävää hän on ratkonut oikein kultakin kurssilta.


## Käyttöohjeet
Kloonaa repositio ja luo kloonaamaasi kansioon .env-tiedosto. Tiedostosta tulee löytyä seuraavat  määrittelyt:

DATABASE_URL=postgresql:///(käyttäjänimi) jossa käyttäjänimi tulee korvata omalla käyttäjänimelläsi sekä

SEC_KEY=(itse generoimasi salainen avain)

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
