from app import app
from db_setup import init_db, db_session
from forms import JusticeSearchForm, CompanyForm
from flask import flash, render_template, request, redirect
from models import Company, Insolvency_Events, Konkurz_Events, Predmet_Podnikani, Predmety_Podnikani_Association, Predmet_Cinnosti, Predmety_Cinnosti_Association 
from models import Zakladni_Kapital, Akcie, Nazvy, Sidlo, Sidlo_Association, Pravni_Forma_Association_v2, Pravni_Formy, Statutarni_Organ_Association, Statutarni_Organy, Pocty_Clenu_Organu
from models import Zpusob_Jednani_Association, Zpusob_Jednani, Statutarni_Organ_Clen_Association, Fyzicka_Osoba, Spolecnici_Association, Podily_Association, Druhy_Podilu, Pravnicka_Osoba
from models import Prokurista_Association, Jediny_Akcionar_Association, Prokura_Common_Text_Association, Soudni_Zapisy, Ucel, Ucel_Association
from models import Adresy_v2
from tables import Results

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    search = JusticeSearchForm(request.form)
    print(search)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)

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

    pravni_forma = search.pravni_forma_search.data
    pravni_forma_actual_or_full = search.pravni_forma_actual.data
    
    soud = search.soud_search.data
    soud_actual_or_full = search.soud_search_actual.data

    insolvent_only = search.insolvent_only_search.data
    
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
        return render_template("results2.html", results=results, form=search, zapsano_od=zapsano_od, zapsano_do=zapsano_do)

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

if __name__ == '__main__':
    app.run()