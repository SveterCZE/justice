# test.py
from app import app
from db_setup import init_db, db_session
from forms import JusticeSearchForm, CompanyForm
from flask import flash, render_template, request, redirect
# from models import Company, Soud
from models import Company, Obce, Ulice, Insolvency_Events, Predmet_Podnikani, Predmety_Podnikani_Association, Predmet_Cinnosti, Predmety_Cinnosti_Association, Zakladni_Kapital, Akcie, Nazvy, Sidlo, Sidlo_Association, Pravni_Forma_Association_v2, Pravni_Formy, Statutarni_Organ_Association, Statutarni_Organy, Pocty_Clenu_Organu, Zpusob_Jednani_Association, Zpusob_Jednani
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
    oddil = search.oddil_search.data
    oddil_search_method = search.oddil_search_selection.data
    vlozka = search.vlozka_search.data
    vlozka_search_method = search.vlozka_search_selection.data
    obec = search.obec_search.data
    obec_search_method = search.obec_search_selection.data
    ulice = search.ulice_search.data
    ulice_search_method = search.ulice_search_selection.data
    pravni_forma = search.pravni_forma_search.data
    soud = search.soud_search.data
    insolvent_only = search.insolvent_only_search.data
    zapsano_od = search.zapis_od.data
    zapsano_do = search.zapis_do.data
    qry = Company.query
    # if insolvent_only == False:
    #     qry = Company.query.join(Obce, Company.obec).join(Ulice, Company.ulice).join(Pravni_Forma, Company.pravni_forma).join(Insolvency_Events, isouter=True)
    # else:
    #     qry = Company.query.join(Obce, Company.obec).join(Ulice, Company.ulice).join(Pravni_Forma, Company.pravni_forma).join(Insolvency_Events, Company.insolvence)
    if ico:
        if ico_search_method == "text_anywhere":
            qry = qry.filter(Company.ico.contains(ico))
        elif ico_search_method == "text_beginning":
            qry = qry.filter(Company.ico.like(f'{ico}%'))
        elif ico_search_method == "text_exact":
            qry = qry.filter(Company.ico == ico)
    if nazev:
        if nazev_search_method == "text_anywhere":
            qry = qry.filter(Company.nazev.contains(nazev))
        elif nazev_search_method == "text_beginning":
            qry = qry.filter(Company.nazev.like(f'{nazev}%'))
        elif nazev_search_method == "text_exact":
            qry = qry.filter(Company.nazev == nazev)
    if oddil:
        if oddil_search_method == "text_anywhere":
            qry = qry.filter(Company.oddil.contains(oddil))
        elif oddil_search_method == "text_beginning":
            qry = qry.filter(Company.oddil.like(f'{oddil}%'))
        elif oddil_search_method == "text_exact":
            qry = qry.filter(Company.oddil == oddil)
        # qry = qry.filter(Company.oddil.contains(oddil))
    if vlozka:
        if vlozka_search_method == "text_anywhere":
            qry = qry.filter(Company.vlozka.contains(vlozka))
        elif vlozka_search_method == "text_beginning":
            qry = qry.filter(Company.vlozka.like(f'{vlozka}%'))
        elif vlozka_search_method == "text_exact":
            qry = qry.filter(Company.vlozka == vlozka)

        # qry = qry.filter(Company.vlozka.contains(vlozka))
    if obec:
        qry = qry.join(Obce, Company.obec)
        if obec_search_method == "text_anywhere":
            qry = qry.filter(Obce.obec_jmeno.contains(obec))
        elif obec_search_method == "text_beginning":
            qry = qry.filter(Obce.obec_jmeno.like(f'{obec}%'))
        elif obec_search_method == "text_exact":
            qry = qry.filter(Obce.obec_jmeno == obec)
        # qry = qry.filter(Obce.obec_jmeno.contains(obec))
    if ulice:
        qry = qry.join(Ulice, Company.ulice)
        if ulice_search_method == "text_anywhere":
            qry = qry.filter(Ulice.ulice_jmeno.contains(ulice))
        elif ulice_search_method == "text_beginning":
            qry = qry.filter(Ulice.ulice_jmeno.like(f'{ulice}%'))
        elif ulice_search_method == "text_exact":
            qry = qry.filter(Ulice.ulice_jmeno == ulice)
        # qry = qry.filter(Ulice.ulice_jmeno.contains(ulice))
    if pravni_forma:
        qry = qry.join(Pravni_Forma, Company.pravni_forma)
        qry = qry.filter(Pravni_Forma.pravni_forma.contains(pravni_forma))
    if soud:
        qry = qry.filter(Company.soud.contains(soud))
    if zapsano_od:
        qry = qry.filter(Company.zapis >= zapsano_od)
    if zapsano_do:
        qry = qry.filter(Company.zapis <= zapsano_do)

    results = qry.all()
        # else:
        #     qry = db_session.query(Company)
        #     results = qry.all()
    # else:
    #     qry = db_session.query(Company)
    #     results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')

    else:
        table = Results(results)
        table.border = True
        # return render_template('results.html', table=table)
        return render_template("results2.html", results=results, form=search, zapsano_od=zapsano_od, zapsano_do=zapsano_do)

def search_results_BACKUP(search):
    results = []
    search_string = search.data['search']

    if search_string:
        # if search.data['select'] == 'soud':
        #     qry = db_session.query(Company, Soud).filter(
        #         Soud.id==Company.soud_id).filter(
        #             Soud.name.contains(search_string))
        #     results = [item[0] for item in qry.all()]
        if search.data['select'] == 'nazev':
            qry = db_session.query(Company).filter(
                Company.nazev.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'ico':
            qry = db_session.query(Company).filter(
                Company.ico.contains(search_string))
            results = qry.all()
        else:
            qry = db_session.query(Company)
            results = qry.all()
    else:
        qry = db_session.query(Company)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')

    else:
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)


@app.route("/<int:ico>", methods=['GET', 'POST'])
def extract(ico):
    qry = Company.query.join(Obce, Company.obec).join(Ulice, Company.ulice).join(Insolvency_Events, isouter=True)
    # qry = Company.query.join(Obce, Company.obec).join(Ulice, Company.ulice).join(Pravni_Forma, Company.pravni_forma).join(Insolvency_Events, isouter=True)
    # qry = Company.query.join(Obce, Company.obec).join(Ulice, Company.ulice).join(Pravni_Forma, Company.pravni_forma).join(Insolvency_Events, Company.insolvence, isouter=True).join(Predmet_Podnikani, Company.predmet_podnikani).join(Predmet_Cinnosti, Company.predmet_cinnosti)
    qry = qry.filter(Company.ico == ico)
    # qry = qry.filter(Company.nazev.contains("prigo"))
    # qry = Obce.query
    results = qry.all()
    return render_template("extract.html", ico = ico, results = results)

@app.route("/<int:ico>-actual", methods=['GET', 'POST'])
def extract_actual(ico):
    qry = Company.query.join(Obce, Company.obec).join(Ulice, Company.ulice).join(Insolvency_Events, isouter=True)
    # qry = Company.query.join(Obce, Company.obec).join(Ulice, Company.ulice).join(Pravni_Forma, Company.pravni_forma).join(Insolvency_Events, isouter=True)
    # qry = Company.query.join(Obce, Company.obec).join(Ulice, Company.ulice).join(Pravni_Forma, Company.pravni_forma).join(Insolvency_Events, Company.insolvence, isouter=True).join(Predmet_Podnikani, Company.predmet_podnikani).join(Predmet_Cinnosti, Company.predmet_cinnosti)
    qry = qry.filter(Company.ico == ico)
    # qry = qry.filter(Company.nazev.contains("prigo"))
     # qry = Obce.query
    results = qry.all()
    return render_template("extract-actual.html", ico = ico, results = results)


@app.route('/new_company', methods=['GET', 'POST'])
def new_company():
    """
    Add a new company
    """
    form = CompanyForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the album
        company = Company()
        save_changes(company, form, new=True)
        flash('Company created successfully!')
        return redirect('/')
    return render_template('new_company.html', form=form)

def save_changes(company, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    # soud = Soud()
    # soud.name = form.soud.data

    # company.soud = soud
    company.soud = form.soud.data
    company.ico = form.ico.data
    company.nazev = form.nazev.data
    company.sidlo = form.sidlo.data
    company.zapis = form.zapis.data
    company.oddil = form.oddil.data
    company.vlozka = form.vlozka.data
    company.vymaz = form.vymaz.data
    if new:
        # Add the new album to the database
        db_session.add(company)
    # commit the data to the database
    db_session.commit()


if __name__ == '__main__':
    app.run()