from app import app
from forms import GeneralSearchForm, JusticeSearchForm, CompanyForm, PersonSearchForm, EntitySearchForm
from flask import flash, render_template, request, redirect
from models import Company, Insolvency_Events, Konkurz_Events, Predmet_Podnikani, Predmety_Podnikani_Association, Predmet_Cinnosti, Predmety_Cinnosti_Association, Ubo
from models import Zakladni_Kapital, Akcie, Nazvy, Sidlo, Sidlo_Association, Pravni_Forma_Association_v2, Pravni_Formy, Statutarni_Organ_Association, Statutarni_Organy, Pocty_Clenu_Organu
from models import Zpusob_Jednani_Association, Zpusob_Jednani, Statutarni_Organ_Clen_Association, Fyzicka_Osoba, Spolecnici_Association, Podily_Association, Druhy_Podilu, Pravnicka_Osoba
from models import Prokurista_Association, Dozorci_Rada_Clen_Association, Jediny_Akcionar_Association, Prokura_Common_Text_Association, Soudni_Zapisy, Ucel, Ucel_Association
from models import Adresy_v2, Uvolneny_Podil_Association, Spolecny_Podil_Association, Podilnici_Association, Criminal_Records, Dozorci_Rada_Association
from tables import Results
from sqlalchemy.sql import select
from sqlalchemy.sql import text
from sqlalchemy import create_engine

@app.route('/', methods=['GET', 'POST'])
def index():
    search = JusticeSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('search_form.html', form=search)

@app.route('/osoby', methods=['GET', 'POST'])
def search_person():
    search = PersonSearchForm(request.form)
    if request.method == 'POST':
        return search_results_person(search)

    return render_template('search_form_person.html', form=search)

@app.route('/entity', methods=['GET', 'POST'])
def search_entity():
    search = EntitySearchForm(request.form)
    if request.method == 'POST':
        return search_results_entity(search)

    return render_template('search_form_entity.html', form=search)


@app.route('/results_person')
def search_results_person(search):
    result = []

    first_name = search.fist_name_search.data
    first_name_search_method = search.fist_name_search_selection.data

    surname = search.surname_search.data
    surname_search_method = search.surname_search_selection.data

    birthday = search.birthday.data

    obec = search.obec_search.data
    obec_search_method = search.obec_search_selection.data

    ulice = search.ulice_search.data
    ulice_search_method = search.ulice_search_selection.data

    co = search.co_search.data
    co_search_method = search.co_search_selection.data

    cp = search.cp_search.data
    cp_search_method = search.cp_search_selection.data

    actual_selection = search.person_actual_selection.data

    qry = Fyzicka_Osoba.query

    if first_name:
        if first_name_search_method == "text_anywhere":
            qry = qry.filter(Fyzicka_Osoba.jmeno.contains(first_name))
        elif first_name_search_method == "text_beginning":
            qry = qry.filter(Fyzicka_Osoba.jmeno.like(f'{first_name}%'))
        elif first_name_search_method == "text_exact":
            qry = qry.filter(Fyzicka_Osoba.jmeno == first_name)

    if surname:
        if surname_search_method == "text_anywhere":
            qry = qry.filter(Fyzicka_Osoba.prijmeni.contains(surname))
        elif surname_search_method == "text_beginning":
            qry = qry.filter(Fyzicka_Osoba.prijmeni.like(f'{surname}%'))
        elif surname_search_method == "text_exact":
            qry = qry.filter(Fyzicka_Osoba.prijmeni == surname)

    if obec:
        qry = qry.join(Adresy_v2, Fyzicka_Osoba.adresa)
        if obec_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.obec.contains(obec))
        elif obec_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.obec.like(f'{obec}%'))
        elif obec_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.obec == obec)

    if ulice:
        qry = qry.join(Adresy_v2, Fyzicka_Osoba.adresa)
        if ulice_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.ulice.contains(ulice))
        elif ulice_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.ulice.like(f'{ulice}%'))
        elif ulice_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.ulice == ulice)

    if cp:
        qry = qry.join(Adresy_v2, Fyzicka_Osoba.adresa)
        if cp_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.cisloPo.contains(cp))
        elif cp_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.cisloPo.like(f'{cp}%'))
        elif cp_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.cisloPo == cp)

    if co:
        qry = qry.join(Adresy_v2, Fyzicka_Osoba.adresa)
        if co_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.cisloOr.contains(co))
        elif co_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.cisloOr.like(f'{co}%'))
        elif co_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.cisloOr == co)

    if birthday:
        qry = qry.filter(Fyzicka_Osoba.datum_naroz == birthday)

    results = qry.all()
    print(results)

    if not results:
        flash('No results found!')
        return redirect('/osoby')

    else:
        table = Results(results)
        table.border = True
        return render_template("results_persons.html", results=results, form=search, show_form = True, selection_method = actual_selection)

@app.route('/results_entity')
def search_results_entity(search):
    entity_name = search.entity_name_search.data
    entity_name_search_method = search.entity_name_search_selection.data

    entity_number = search.entity_number_search.data
    entity_number_search_method = search.entity_number_search_selection.data

    obec = search.obec_search.data
    obec_search_method = search.obec_search_selection.data

    ulice = search.ulice_search.data
    ulice_search_method = search.ulice_search_selection.data

    co = search.co_search.data
    co_search_method = search.co_search_selection.data

    cp = search.cp_search.data
    cp_search_method = search.cp_search_selection.data

    actual_selection = search.entity_actual_selection.data

    qry = Pravnicka_Osoba.query

    if entity_number:
        qry1 = Pravnicka_Osoba.query
        if entity_number_search_method == "text_anywhere":
            qry = qry.filter(Pravnicka_Osoba.ico.contains(entity_number))
            qry1 = qry1.filter(Pravnicka_Osoba.reg_cislo.contains(entity_number))
        elif entity_number_search_method == "text_beginning":
            qry = qry.filter(Pravnicka_Osoba.ico.like(f'{entity_number}%'))
            qry1 = qry1.filter(Pravnicka_Osoba.reg_cislo.like(f'{entity_number}%'))
        elif entity_number_search_method == "text_exact":
            qry = qry.filter(Pravnicka_Osoba.ico == entity_number)
            qry1 = qry1.filter(Pravnicka_Osoba.reg_cislo == entity_number)
        qry = qry.union(qry1)

    if entity_name:
        if entity_name_search_method == "text_anywhere":
            qry = qry.filter(Pravnicka_Osoba.nazev.contains(entity_name))
        elif entity_name_search_method == "text_beginning":
            qry = qry.filter(Pravnicka_Osoba.nazev.like(f'{entity_name}%'))
        elif entity_name_search_method == "text_exact":
            qry = qry.filter(Pravnicka_Osoba.nazev == entity_name)

    if obec:
        qry = qry.join(Adresy_v2, Pravnicka_Osoba.adresa)
        if obec_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.obec.contains(obec))
        elif obec_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.obec.like(f'{obec}%'))
        elif obec_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.obec == obec)

    if ulice:
        qry = qry.join(Adresy_v2, Pravnicka_Osoba.adresa)
        if ulice_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.ulice.contains(ulice))
        elif ulice_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.ulice.like(f'{ulice}%'))
        elif ulice_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.ulice == ulice)

    if cp:
        qry = qry.join(Adresy_v2, Pravnicka_Osoba.adresa)
        if cp_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.cisloPo.contains(cp))
        elif cp_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.cisloPo.like(f'{cp}%'))
        elif cp_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.cisloPo == cp)

    if co:
        qry = qry.join(Adresy_v2, Pravnicka_Osoba.adresa)
        if co_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.cisloOr.contains(co))
        elif co_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.cisloOr.like(f'{co}%'))
        elif co_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.cisloOr == co)

    results = qry.all()
    print(results)

    if not results:
        flash('No results found!')
        return redirect('/entity')

    else:
        table = Results(results)
        table.border = True
        return render_template("results_entities.html", results=results, form=search, show_form = True, selection_method = actual_selection)


@app.route('/results')
def search_results(search):
    results = []

    ico = search.ico_search.data
    ico_search_method = search.ico_search_selection.data

    nazev = search.nazev_subjektu.data
    nazev_search_method = search.nazev_subjektu_selection.data
    nazev_actual_or_full = search.nazev_search_actual.data

    oddil = search.oddil_search.data
    oddil_search_method = search.oddil_search_selection.data
    oddil_actual_or_full = search.oddil_search_actual.data

    vlozka = search.vlozka_search.data
    vlozka_search_method = search.vlozka_search_selection.data
    vlozka_actual_or_full = search.vlozka_search_actual.data

    obec = search.obec_search.data
    obec_search_method = search.obec_search_selection.data
    obec_actual_or_full = search.obec_search_actual.data

    ulice = search.ulice_search.data
    ulice_search_method = search.ulice_search_selection.data
    ulice_actual_or_full = search.ulice_search_actual.data

    co = search.co_search.data
    co_search_method = search.co_search_selection.data
    co_actual_or_full = search.co_search_actual.data

    cp = search.cp_search.data
    cp_search_method = search.cp_search_selection.data
    cp_actual_or_full = search.cp_search_actual.data

    pravni_forma = search.pravni_forma_search.data
    pravni_forma_actual_or_full = search.pravni_forma_actual.data

    soud = search.soud_search.data
    soud_actual_or_full = search.soud_search_actual.data

    insolvent_only = search.insolvent_only_search.data

    criminal_record_only = search.criminal_record_only_search.data

    zapsano_od = search.zapis_od.data
    zapsano_do = search.zapis_do.data

    qry = Company.query

    if insolvent_only:
        qry = qry.join(Insolvency_Events, Company.insolvence)
        qry = qry.filter(Insolvency_Events.vymaz_datum == 0)
        qry_konkurz = Company.query
        qry_konkurz = qry_konkurz.join(Konkurz_Events, Company.konkurz)
        qry_konkurz = qry_konkurz.filter(Konkurz_Events.vymaz_datum == 0)
        qry = qry.union(qry_konkurz)

    if criminal_record_only:
        qry = qry.join(Criminal_Records, Company.criminal_record)

    if ico:
        if ico_search_method == "text_anywhere":
            qry = qry.filter(Company.ico.contains(ico))
        elif ico_search_method == "text_beginning":
            qry = qry.filter(Company.ico.like(f'{ico}%'))
        elif ico_search_method == "text_exact":
            qry = qry.filter(Company.ico == ico)

    if nazev:
        qry = qry.join(Nazvy, Company.obchodni_firma)
        if nazev_actual_or_full == "actual_results":
            qry = qry.filter(Nazvy.vymaz_datum == 0)
        if nazev_search_method == "text_anywhere":
            qry = qry.filter(Nazvy.nazev_text.contains(nazev))
        elif nazev_search_method == "text_beginning":
            qry = qry.filter(Nazvy.nazev_text.like(f'{nazev}%'))
        elif nazev_search_method == "text_exact":
            qry = qry.filter(Nazvy.nazev_text == nazev)

    if oddil:
        qry = qry.join(Soudni_Zapisy, Company.soudni_zapis)
        if oddil_actual_or_full == "actual_results":
            qry = qry.filter(Soudni_Zapisy.vymaz_datum == 0)
        if oddil_search_method == "text_anywhere":
            qry = qry.filter(Company.oddil.contains(oddil))
        elif oddil_search_method == "text_beginning":
            qry = qry.filter(Company.oddil.like(f'{oddil}%'))
        elif oddil_search_method == "text_exact":
            qry = qry.filter(Company.oddil == oddil)

    if vlozka:
        qry = qry.join(Soudni_Zapisy, Company.soudni_zapis)
        if vlozka_actual_or_full == "actual_results":
            qry = qry.filter(Soudni_Zapisy.vymaz_datum == 0)
        if vlozka_search_method == "text_anywhere":
            qry = qry.filter(Soudni_Zapisy.vlozka.contains(vlozka))
        elif vlozka_search_method == "text_beginning":
            qry = qry.filter(Soudni_Zapisy.vlozka.like(f'{vlozka}%'))
        elif vlozka_search_method == "text_exact":
            qry = qry.filter(Soudni_Zapisy.vlozka == vlozka)

    if obec:
        qry = qry.join(Sidlo_Association, Company.sidlo_text)
        if obec_actual_or_full == "actual_results":
            qry = qry.filter(Sidlo_Association.vymaz_datum == 0)
        qry = qry.join(Adresy_v2, Sidlo_Association.sidlo_text)
        if obec_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.obec.contains(obec))
        elif obec_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.obec.like(f'{obec}%'))
        elif obec_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.obec == obec)

    if ulice:
        qry = qry.join(Sidlo_Association, Company.sidlo_text)
        if ulice_actual_or_full == "actual_results":
            qry = qry.filter(Sidlo_Association.vymaz_datum == 0)
        qry = qry.join(Adresy_v2, Sidlo_Association.sidlo_text)
        if ulice_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.ulice.contains(ulice))
        elif ulice_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.ulice.like(f'{ulice}%'))
        elif ulice_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.ulice == ulice)

    if cp:
        qry = qry.join(Sidlo_Association, Company.sidlo_text)
        if cp_actual_or_full == "actual_results":
            qry = qry.filter(Sidlo_Association.vymaz_datum == 0)
        qry = qry.join(Adresy_v2, Sidlo_Association.sidlo_text)
        if cp_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.cisloPo.contains(cp))
        elif cp_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.cisloPo.like(f'{cp}%'))
        elif cp_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.cisloPo == cp)

    if co:
        qry = qry.join(Sidlo_Association, Company.sidlo_text)
        if co_actual_or_full == "actual_results":
            qry = qry.filter(Sidlo_Association.vymaz_datum == 0)
        qry = qry.join(Adresy_v2, Sidlo_Association.sidlo_text)
        if co_search_method == "text_anywhere":
            qry = qry.filter(Adresy_v2.cisloOr.contains(co))
        elif co_search_method == "text_beginning":
            qry = qry.filter(Adresy_v2.cisloOr.like(f'{co}%'))
        elif co_search_method == "text_exact":
            qry = qry.filter(Adresy_v2.cisloOr == co)

    if pravni_forma:
        qry = qry.join(Pravni_Forma_Association_v2, Company.pravni_forma_text)
        if pravni_forma_actual_or_full == "actual_results":
            qry = qry.filter(Pravni_Forma_Association_v2.vymaz_datum == 0)
        qry = qry.join(Pravni_Formy, Pravni_Forma_Association_v2.pravni_forma_text)
        qry = qry.filter(Pravni_Formy.pravni_forma == pravni_forma)

    if soud:
        qry = qry.join(Soudni_Zapisy, Company.soudni_zapis)
        if soud_actual_or_full == "actual_results":
            qry = qry.filter(Soudni_Zapisy.vymaz_datum == 0)
        qry = qry.filter(Soudni_Zapisy.soud == soud)

    if zapsano_od:
        qry = qry.filter(Company.zapis >= zapsano_od)
    if zapsano_do:
        qry = qry.filter(Company.zapis <= zapsano_do)

    results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')

    else:
        table = Results(results)
        table.border = True
        return render_template("results2.html", results=results, form=search, zapsano_od=zapsano_od, zapsano_do=zapsano_do, show_form = True)



@app.route('/results-sidlo-<int:adresa_id>', methods=['GET', 'POST'])
def search_results_sidlo(adresa_id):
    search = JusticeSearchForm(request.form)

    results = []
    qry = Company.query
    qry = qry.join(Sidlo_Association, Company.sidlo_text)
    qry = qry.filter(Sidlo_Association.vymaz_datum == 0)
    qry = qry.join(Adresy_v2, Sidlo_Association.sidlo_text)
    qry = qry.filter(Adresy_v2.id == adresa_id)
    results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')

    else:
        table = Results(results)
        table.border = True
        return render_template("results2.html", results=results, form=search, show_form = False)


# UBO reults
@app.route('/results-ubo-<int:ubo_id>', methods=['GET', 'POST'])
def search_results_ubo(ubo_id):
    search = JusticeSearchForm(request.form)

    results = []
    qry = Company.query
    qry = qry.join(Ubo, Company.ubo)
    qry = qry.filter(Ubo.vymaz_datum == 0)
    qry = qry.join(Fyzicka_Osoba, Ubo.jmeno)
    qry = qry.filter(Fyzicka_Osoba.id == ubo_id)
    results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')

    else:
        table = Results(results)
        table.border = True
        return render_template("results2.html", results=results, form=search, show_form = False)


@app.route("/<int:ico>", methods=['GET', 'POST'])
def extract(ico):
    qry = Company.query
    qry = qry.filter(Company.ico == ico)
    results = qry.all()
    return render_template("extract.html", ico = ico, results = results)

@app.route("/<int:ico>-actual", methods=['GET', 'POST'])
def extract_actual(ico):
    qry = Company.query
    qry = qry.filter(Company.ico == ico)
    results = qry.all()
    return render_template("extract-actual.html", ico = ico, results = results)

@app.route("/trivia", methods=['GET', 'POST'])
def trivia():
    number_entities = count_number_entries()
    return render_template("trivia.html", number_entities = number_entities)

@app.route("/most_common_addresses", methods=['GET', 'POST'])
def find_most_common_addresses():
    most_common_addresses = count_common_addresses()
    return render_template("most_common_addresses.html", most_common_addresses = most_common_addresses)

@app.route("/oldest_companies", methods=['GET', 'POST'])
def find_oldest_companies():
    oldest_companies = count_oldest_companies()
    return render_template("oldest_companies.html", oldest_companies = oldest_companies)

@app.route("/most_common_purpose", methods=['GET', 'POST'])
def find_most_common_purpose():
    most_common_purpose = count_common_purpose()
    return render_template("most_common_purpose.html", most_common_purpose = most_common_purpose)

@app.route("/most_common_ubo", methods=['GET', 'POST'])
def find_most_common_ubo():
    most_common_ubo = count_common_ubo()
    return render_template("most_common_ubo.html", most_common_ubo = most_common_ubo)

@app.route("/most_common_business", methods=['GET', 'POST'])
def find_most_common_business():
    most_common_business = count_common_business()
    return render_template("most_common_business.html", most_common_business = most_common_business)

@app.route("/most_common_activity", methods=['GET', 'POST'])
def find_most_common_activity():
    most_common_activity = count_common_activity()
    return render_template("most_common_activity.html", most_common_activity = most_common_activity)

@app.route("/most_common_degree", methods=['GET', 'POST'])
def find_most_common_degree():
    most_common_degree_before = count_common_degrees("before")
    most_common_degree_after = count_common_degrees("after")
    return render_template("most_common_degree.html", most_common_degree_before = most_common_degree_before, most_common_degree_after = most_common_degree_after)

@app.route("/oldest_persons", methods=['GET', 'POST'])
def find_oldest_persons():
    connected_list = count_oldest_shareholders() + count_oldest_executieves() + count_oldest_sole_shareholders() + count_oldest_prokurists() + count_oldest_supervisory_members()
    sorted_list = sorted(connected_list, key=lambda elem: elem[2])
    return render_template("oldest_persons.html", oldest_persons_list=sorted_list[:100])

@app.route("/longest_registered_persons", methods=['GET', 'POST'])
def find_longest_registered_persons():
    connected_list = count_longest_registered_executives() + count_longest_registered_shareholders() + count_longest_registered_sole_shareholders() + count_longest_registered_prokurists() + count_longest_registered_supervsiory_members()
    sorted_list = sorted(connected_list, key=lambda elem: elem[6])
    return render_template("longest_registered_persons.html", longest_registered_persons_list=sorted_list[:100])

@app.route("/youngest_persons",  methods=['GET', 'POST'])
def find_younges_persons():
    connected_list = count_youngest_shareholders() + count_youngest_executieves() + count_youngest_sole_shareholders() + count_youngest_prokurists() + count_youngest_supervisory_members()
    sorted_list = sorted(connected_list, key=lambda elem: elem[2], reverse=True)
    return render_template("youngest_persons.html", youngest_persons_list=sorted_list[:100])

def count_number_entries():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT COUNT(id) FROM companies;")
    entries_number = conn.execute(text_instruction).fetchall()
    conn.close()
    return entries_number[0][0]

def count_common_addresses():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT sidlo_id, COUNT(`sidlo_id`) AS `value_occurrence` FROM sidlo_relation INNER JOIN adresy_v2 ON sidlo_relation.sidlo_id=adresy_v2.id WHERE vymaz_datum = 0 GROUP BY `sidlo_id` ORDER BY `value_occurrence` DESC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    addresses_frequency = []
    for elem in result:
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[0])
        selected_address = qry.all()
        addresses_frequency.append((selected_address[0], elem[1], elem[0]))
    conn.close()
    return addresses_frequency

def count_common_business():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT predmet_podnikani_id, COUNT(`predmet_podnikani_id`) AS `value_occurrence` FROM predmety_podnikani_relation INNER JOIN predmety_podnikani ON predmety_podnikani_relation.predmet_podnikani_id=predmety_podnikani.id WHERE vymaz_datum = 0 GROUP BY `predmet_podnikani_id` ORDER BY `value_occurrence` DESC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    business_frequency = []
    for elem in result:
        qry = Predmet_Podnikani.query
        qry = qry.filter(Predmet_Podnikani.id == elem[0])
        selected_business = qry.all()
        business_frequency.append((selected_business[0].predmet_podnikani, elem[1]))
    conn.close()
    return business_frequency

def count_common_activity():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT predmet_cinnosti_id, COUNT(`predmet_cinnosti_id`) AS `value_occurrence` FROM predmety_cinnosti_relation INNER JOIN predmety_cinnosti ON predmety_cinnosti_relation.predmet_cinnosti_id=predmety_cinnosti.id WHERE vymaz_datum = 0 GROUP BY `predmet_cinnosti_id` ORDER BY `value_occurrence` DESC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    activity_frequency = []
    for elem in result:
        qry = Predmet_Cinnosti.query
        qry = qry.filter(Predmet_Cinnosti.id == elem[0])
        selected_activity = qry.all()
        activity_frequency.append((selected_activity[0].predmet_cinnosti, elem[1]))
    conn.close()
    return activity_frequency

def count_common_purpose():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT ucel_id, COUNT(`ucel_id`) AS `value_occurrence` FROM ucel_relation INNER JOIN ucel ON ucel_relation.ucel_id=ucel.id WHERE vymaz_datum = 0 GROUP BY `ucel_id` ORDER BY `value_occurrence` DESC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    addresses_frequency = []
    for elem in result:
        qry = Ucel.query
        qry = qry.filter(Ucel.id == elem[0])
        selected_purpose = qry.all()
        addresses_frequency.append((selected_purpose[0].ucel, elem[1]))
    conn.close()
    return addresses_frequency

def count_common_ubo():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT UBO_id, COUNT(`UBO_id`) AS `value_occurrence` FROM ubo INNER JOIN fyzicke_osoby ON ubo.UBO_id=fyzicke_osoby.id WHERE vymaz_datum = 0 GROUP BY `UBO_id` ORDER BY `value_occurrence` DESC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    ubo_frequency = []
    for elem in result:
        qry = Fyzicka_Osoba.query
        qry = qry.filter(Fyzicka_Osoba.id == elem[0])
        selected_ubo = qry.all()
        ubo_frequency.append((selected_ubo[0], elem[1], elem[0]))
    conn.close()
    return ubo_frequency

def count_common_degrees(method):
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    if method == "before":
        text_instruction = text("SELECT titul_pred, COUNT(`titul_pred`) AS `value_occurrence` FROM fyzicke_osoby GROUP BY `titul_pred` ORDER BY `value_occurrence` DESC LIMIT 100;")
    else:
        text_instruction = text("SELECT titul_za, COUNT(`titul_za`) AS `value_occurrence` FROM fyzicke_osoby GROUP BY `titul_za` ORDER BY `value_occurrence` DESC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    degree_frequency = []
    for elem in result:
        degree_frequency.append((elem[0], elem[1]))
    return degree_frequency[1:]

def count_oldest_companies():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT id from companies ORDER BY zapis ASC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    oldest_companies = []
    for elem in result:
        qry = Company.query
        qry = qry.filter(Company.id == elem[0])
        selected_company = qry.all()
        oldest_companies.append((selected_company[0].nazev, selected_company[0].zapis, selected_company[0].ico))
    return oldest_companies

def count_oldest_shareholders():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, spolecnici.zapis_datum, company_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN spolecnici ON spolecnici.spolecnik_fo_id=fyzicke_osoby.id WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '9999-10-10' ELSE datum_naroz END ASC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    oldest_shareholders = []
    for elem in result:
        qry = Company.query
        qry = qry.filter(Company.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        oldest_shareholders.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "společník"))
    return oldest_shareholders

def count_oldest_executieves():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, statutarni_organ_clen_relation.zapis_datum, statutarni_organ_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN statutarni_organ_clen_relation ON statutarni_organ_clen_relation.osoba_id=fyzicke_osoby.id  WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '9999-10-10' ELSE datum_naroz END ASC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    oldest_executives = []
    for elem in results:
        qry = Company.query
        qry = qry.join(Statutarni_Organ_Association, Company.statutarni_organ_text)
        qry = qry.filter(Statutarni_Organ_Association.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        oldest_executives.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "člen statutárního orgánu"))
    return oldest_executives

def count_oldest_prokurists():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, prokuriste.zapis_datum, company_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN prokuriste ON prokuriste.prokurista_fo_id=fyzicke_osoby.id WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '9999-10-10' ELSE datum_naroz END ASC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    oldest_prokurists = []
    for elem in results:
        qry = Company.query
        qry = qry.filter(Company.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        oldest_prokurists.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "prokurista"))
    return oldest_prokurists

def count_oldest_sole_shareholders():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, jediny_akcionar.zapis_datum, company_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN jediny_akcionar ON jediny_akcionar.akcionar_fo_id=fyzicke_osoby.id WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '9999-10-10' ELSE datum_naroz END ASC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    oldest_sole_shareholders = []
    for elem in results:
        qry = Company.query
        qry = qry.filter(Company.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        oldest_sole_shareholders.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "jediný akcionář"))
    return oldest_sole_shareholders

def count_oldest_supervisory_members():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, dr_organ_clen_relation.zapis_datum, dozorci_rada_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN dr_organ_clen_relation ON dr_organ_clen_relation.osoba_id=fyzicke_osoby.id  WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '9999-10-10' ELSE datum_naroz END ASC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    oldest_supervisory_members = []
    for elem in results:
        qry = Company.query
        qry = qry.join(Dozorci_Rada_Association, Company.dozorci_rada_text)
        qry = qry.filter(Dozorci_Rada_Association.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        oldest_supervisory_members.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "člen dozorčí rady"))
    return oldest_supervisory_members

def count_youngest_shareholders():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, spolecnici.zapis_datum, company_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN spolecnici ON spolecnici.spolecnik_fo_id=fyzicke_osoby.id WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '1111-10-10' ELSE datum_naroz END DESC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    youngest_shareholders = []
    for elem in result:
        qry = Company.query
        qry = qry.filter(Company.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        youngest_shareholders.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "společník"))
    return youngest_shareholders

def count_youngest_executieves():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, statutarni_organ_clen_relation.zapis_datum, statutarni_organ_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN statutarni_organ_clen_relation ON statutarni_organ_clen_relation.osoba_id=fyzicke_osoby.id  WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '1111-10-10' ELSE datum_naroz END DESC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    youngest_executives = []
    for elem in results:
        qry = Company.query
        qry = qry.join(Statutarni_Organ_Association, Company.statutarni_organ_text)
        qry = qry.filter(Statutarni_Organ_Association.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        youngest_executives.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "člen statutárního orgánu"))
    return youngest_executives

def count_youngest_prokurists():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, prokuriste.zapis_datum, company_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN prokuriste ON prokuriste.prokurista_fo_id=fyzicke_osoby.id WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '1111-10-10' ELSE datum_naroz END DESC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    youngest_prokurists = []
    for elem in results:
        qry = Company.query
        qry = qry.filter(Company.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        youngest_prokurists.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "prokurista"))
    return youngest_prokurists

def count_youngest_sole_shareholders():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, jediny_akcionar.zapis_datum, company_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN jediny_akcionar ON jediny_akcionar.akcionar_fo_id=fyzicke_osoby.id WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '1111-10-10' ELSE datum_naroz END DESC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    youngest_sole_shareholders = []
    for elem in results:
        qry = Company.query
        qry = qry.filter(Company.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        youngest_sole_shareholders.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "jediný akcionář"))
    return youngest_sole_shareholders

def count_youngest_supervisory_members():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, dr_organ_clen_relation.zapis_datum, dozorci_rada_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN dr_organ_clen_relation ON dr_organ_clen_relation.osoba_id=fyzicke_osoby.id  WHERE vymaz_datum = 0 ORDER BY CASE WHEN datum_naroz = 0 THEN '1111-10-10' ELSE datum_naroz END DESC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    youngest_supervisory_members = []
    for elem in results:
        qry = Company.query
        qry = qry.join(Dozorci_Rada_Association, Company.dozorci_rada_text)
        qry = qry.filter(Dozorci_Rada_Association.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        youngest_supervisory_members.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "člen dozorčí rady"))
    return youngest_supervisory_members

def count_longest_registered_shareholders():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, spolecnici.zapis_datum, company_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN spolecnici ON spolecnici.spolecnik_fo_id=fyzicke_osoby.id WHERE vymaz_datum = 0 ORDER BY CASE WHEN zapis_datum = 0 THEN '9999-10-10' ELSE zapis_datum END ASC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    longest_registered_shareholders = []
    for elem in result:
        qry = Company.query
        qry = qry.filter(Company.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        longest_registered_shareholders.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "společník"))
    return longest_registered_shareholders

def count_longest_registered_executives():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, statutarni_organ_clen_relation.zapis_datum, statutarni_organ_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN statutarni_organ_clen_relation ON statutarni_organ_clen_relation.osoba_id=fyzicke_osoby.id  WHERE vymaz_datum = 0 ORDER BY CASE WHEN zapis_datum = 0 THEN '2099-10-10' ELSE zapis_datum END ASC LIMIT 100;")
    result = conn.execute(text_instruction).fetchall()
    longest_registered_executives = []
    for elem in result:
        qry = Company.query
        qry = qry.join(Statutarni_Organ_Association, Company.statutarni_organ_text)
        qry = qry.filter(Statutarni_Organ_Association.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        longest_registered_executives.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "člen statutárního orgánu"))
    return longest_registered_executives

def count_longest_registered_sole_shareholders():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, jediny_akcionar.zapis_datum, company_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN jediny_akcionar ON jediny_akcionar.akcionar_fo_id=fyzicke_osoby.id WHERE vymaz_datum = 0 ORDER BY CASE WHEN zapis_datum = 0 THEN '9999-10-10' ELSE zapis_datum END ASC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    longest_registered_sole_shareholders = []
    for elem in results:
        qry = Company.query
        qry = qry.filter(Company.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        longest_registered_sole_shareholders.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "jediný akcionář"))
    return longest_registered_sole_shareholders

def count_longest_registered_prokurists():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, prokuriste.zapis_datum, company_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN prokuriste ON prokuriste.prokurista_fo_id=fyzicke_osoby.id WHERE vymaz_datum = 0 ORDER BY CASE WHEN zapis_datum = 0 THEN '9999-10-10' ELSE zapis_datum END ASC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    longest_registered_prokurists = []
    for elem in results:
        qry = Company.query
        qry = qry.filter(Company.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        longest_registered_prokurists.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "prokurista"))
    return longest_registered_prokurists

def count_longest_registered_supervsiory_members():
    engine = create_engine('sqlite:///justice.db', echo=True)
    conn = engine.connect()
    text_instruction = text("SELECT jmeno, prijmeni, datum_naroz, dr_organ_clen_relation.zapis_datum, dozorci_rada_id, fyzicke_osoby.adresa_id from fyzicke_osoby INNER JOIN dr_organ_clen_relation ON dr_organ_clen_relation.osoba_id=fyzicke_osoby.id  WHERE vymaz_datum = 0 ORDER BY CASE WHEN zapis_datum = 0 THEN '9999-10-10' ELSE zapis_datum END ASC LIMIT 100;")
    results = conn.execute(text_instruction).fetchall()
    longest_registered_supervisory_members = []
    for elem in results:
        qry = Company.query
        qry = qry.join(Dozorci_Rada_Association, Company.dozorci_rada_text)
        qry = qry.filter(Dozorci_Rada_Association.id == elem[4])
        selected_company = qry.all()
        qry = Adresy_v2.query
        qry = qry.filter(Adresy_v2.id == elem[5])
        selected_address = qry.all()
        longest_registered_supervisory_members.append((elem[0], elem[1], elem[2], selected_company[0].nazev, selected_company[0].ico, selected_address[0], elem[3], "člen dozorčí rady"))
    return longest_registered_supervisory_members

if __name__ == '__main__':
    app.run()