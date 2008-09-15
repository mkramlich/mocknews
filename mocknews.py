#!/usr/bin/env python2.5

from __future__ import with_statement

import math
import random

class Celeb:
    def __init__(self, name):
        self.name = name
        self.gender = 'm'
        self.married = False

class City:
    def __init__(self, name):
        self.name = name

class SportTeam:
    def __init__(self, name):
        self.name = name

class Company:
    def __init__(self, name):
        self.name = name
        self.merged = False
        self.field = None

def apply_template_simple(template, tag, replaceset, should_capitalize=False):
    choice = random.choice(replaceset)
    if should_capitalize:
        choice = choice.capitalize()
    params = {tag:choice,}
    return template % params

def one_company_gen(event):
    hl_tmpl = random.choice(event.templates)
    company = random.choice(companies)
    params = {'company':company.name}
    event.headline = hl_tmpl % params
    return event.headline

def gen_with_one_city(event):
    hl_tmpl = random.choice(event.templates)
    city = random.choice(cities)
    params = {'city':city.name}
    event.headline = hl_tmpl % params
    return event.headline

def gen_with_one_nation(event):
    hl_tmpl = random.choice(event.templates)
    nation_name = random.choice(nations)
    params = {'nation':nation_name}
    event.headline = hl_tmpl % params
    return event.headline

class NewsEvent:
    templates = []

class Invasion(NewsEvent):
    templates = [
        '%(nation.invader)s Declares War On %(nation.invaded)s',
        '%(nation.invader)s Invades %(nation.invaded)s',
        '%(nation.invader)s Occupies %(nation.invaded)s']

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        invader = random.choice(nations)
        n2 = list(nations)
        n2.remove(invader)
        invaded = random.choice(n2)
        params = {'nation.invader':invader, 'nation.invaded':invaded}
        self.headline= hl_tmpl % params
        return self.headline

class Wedding(NewsEvent):
    templates = [
        '%(celeb.1)s Weds %(celeb.2)s',
        '%(celeb.1)s Marries %(celeb.2)s']

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        celeb1 = random.choice(celebs)
        if celeb1.married:
            return
        c2 = list(celebs)
        c2.remove(celeb1)
        if len(c2) == 0:
            return
        celeb2 = random.choice(c2)
        if celeb2.married:
            return
        if celeb1.gender == celeb2.gender:
            return
        params = {'celeb.1':celeb1.name, 'celeb.2':celeb2.name}
        self.headline = hl_tmpl % params
        celeb1.married = celeb2
        celeb2.married = celeb1
        return self.headline

class Divorce(NewsEvent):
    templates = [
        '%(celeb.1)s Divorces %(celeb.2)s',
        '%(celeb.1)s Separates From %(celeb.2)s']

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        celeb1 = random.choice(celebs)
        if not celeb1.married:
            return
        celeb2 = celeb1.married
        params = {'celeb.1':celeb1.name, 'celeb.2':celeb2.name}
        self.headline = hl_tmpl % params
        celeb1.married = None
        celeb2.married = None
        return self.headline

class Beat(NewsEvent):
    templates = [
        '%(sportteam.1)s Beat %(sportteam.2)s',
        '%(sportteam.1)s Crush %(sportteam.2)s']

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        sport = random.choice(sport_values_for_prefix['sport'])
        sport_trait = 'sport:' + sport
        team1 = random.choice(sport_teams_by_trait[sport_trait])
        st2 = list(sport_teams_by_trait[sport_trait])
        st2.remove(team1)
        team2 = random.choice(st2)
        params = {'sportteam.1':team1.name, 'sportteam.2':team2.name}
        self.headline = hl_tmpl % params
        return self.headline

class Merge(NewsEvent):
    templates = [
        '%(company.1)s Merges With %(company.2)s',
        '%(company.1)s Unites With %(company.2)s']

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        field = random.choice(company_values_for_prefix['field'])
        key = 'field:' + field
        company1 = random.choice(companies_by_trait[key])
        if company1.merged:
            return
        cs2 = list(companies_by_trait[key])
        cs2.remove(company1)
        company2 = random.choice(cs2)
        if company2.merged:
            return
        params = {'company.1':company1.name, 'company.2':company2.name}
        self.headline = hl_tmpl % params
        company1.merged = True
        company2.merged = True
        return self.headline

class Layoff(NewsEvent):
    templates = ['%(company)s Lays Off %(qty)s',]

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        company = random.choice(companies)
        base = 1 + random.randrange(75)
        factor = math.pow(10, random.randrange(4))
        qty = int(base * factor)
        params = {'company':company.name, 'qty':qty}
        self.headline = hl_tmpl % params
        return self.headline

class Pileup(NewsEvent):
    templates = ['%(car_count)s Car Pile-Up in %(city)s',]

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        car_count = 5 + random.randrange(20)
        city = random.choice(cities)
        params = {'car_count':car_count, 'city':city.name}
        self.headline = hl_tmpl % params
        return self.headline

class Hurricane(NewsEvent):
    templates = ['Hurricane %(name)s %(verb)s %(city)s',]

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        name = random.choice(hurricane_names)
        verb = random.choice(hurricane_verbs)
        city = random.choice(cities_by_trait['coastal'])
        params = {'name':name, 'verb':verb, 'city':city.name}
        self.headline = hl_tmpl % params
        return self.headline

class Tornado(NewsEvent):
    templates = ['Tornado Hits %(city)s Killing %(qty)s',]

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        city = random.choice(cities_by_trait['tornado'])
        qty = 1 + random.randrange(30)
        params = {'city':city.name, 'qty':qty}
        self.headline = hl_tmpl % params
        return self.headline

class Breakthrough(NewsEvent):
    templates = ['%(disease)s Breakthrough Reported',]

    def gen(self):
        hl_tmpl = random.choice(self.templates)
        self.headline = apply_template_simple(hl_tmpl,'disease',diseases)
        return self.headline

class Bankruptcy(NewsEvent):
    templates = ['%(company)s Enters Bankruptcy',]
    def gen(self):
        return one_company_gen(self)

class CeoResigns(NewsEvent):
    templates = ['%(company)s CEO Resigns',]
    def gen(self):
        return one_company_gen(self)

class ShareholderLawsuit(NewsEvent):
    templates = ['Shareholder Lawsuit Filed Against %(company)s',]
    def gen(self):
        return one_company_gen(self)

class PlaneCrash(NewsEvent):
    templates = ['Plane Crash Near %(city)s',]
    def gen(self):
        return gen_with_one_city(self)

class TrainDerailment(NewsEvent):
    templates = ['Train Derailment Near %(city)s',]
    def gen(self):
        return gen_with_one_city(self)

class Earthquake(NewsEvent):
    templates = ['Earthquake Rocks %(city)s',]
    def gen(self):
        return gen_with_one_city(self)

class Tsunami(NewsEvent):
    templates = ['Tsunami Strikes %(city)s',]
    def gen(self):
        return gen_with_one_city(self)

class PrisonEscape(NewsEvent):
    templates = ['Prison Escape Near %(city)s',]
    def gen(self):
        return gen_with_one_city(self)

class IceShelfBreaksOff(NewsEvent):
    templates = ['Ice Shelf Breaks Off',]
    def gen(self):
        self.headline = random.choice(self.templates)
        return self.headline

class PlanetDiscovered(NewsEvent):
    templates = ['Planet Discovered in %(star)s System',]
    def gen(self):
        hl_tmpl = random.choice(self.templates)
        star = random.choice(stars)
        params = {'star':star}
        self.headline = hl_tmpl % params
        return self.headline

class AnimalSpeciesDeclaredEndangered(NewsEvent):
    templates = ['Rare %(animal)s Declared Endangered',]
    def gen(self):
        hl_tmpl = random.choice(self.templates)
        self.headline = apply_template_simple(hl_tmpl,'animal',animals,True)
        return self.headline

class CrazyManLivesSecretly50YearsInSomeHome(NewsEvent):
    templates = ['Crazy Man Lived in %(home)s for 50 Years in Secret',]
    def gen(self):
        hl_tmpl = random.choice(self.templates)
        self.headline = apply_template_simple(hl_tmpl,'home',homes)
        return self.headline

class MostHatedProfession(NewsEvent):
    templates = ['Polls Indicate %(job)s Most Hated Profession',]
    def gen(self):
        hl_tmpl = random.choice(self.templates)
        self.headline = apply_template_simple(hl_tmpl,'job',jobs)
        return self.headline

class NationElectsLeader(NewsEvent):
    templates = ['%(nation)s Elects New Leader',]
    def gen(self):
        return gen_with_one_nation(self)

class MarketBooming(NewsEvent):
    templates = ['%(market)s Business Booming',]
    def gen(self):
        hl_tmpl = random.choice(self.templates)
        self.headline = apply_template_simple(hl_tmpl,'market',markets)
        return self.headline

class MetalMineDrawsOppositionInCity(NewsEvent):
    templates = ['New %(metal)s Mine Draws Fire in %(city)s',]
    def gen(self):
        hl_tmpl = random.choice(self.templates)
        metal = random.choice(metals)
        city = random.choice(cities)
        params = {'metal':metal, 'city':city.name}
        self.headline = hl_tmpl % params
        return self.headline

class AreaManSeesNothingWrongCrazyVehicle(NewsEvent):
    templates = ['Area Man Sees Nothing Wrong With Homemade Pink Grenade-Launching %(vehicle)s',]
    def gen(self):
        hl_tmpl = random.choice(self.templates)
        self.headline = apply_template_simple(hl_tmpl,'vehicle',vehicles)
        return self.headline

class AnimalsAreForEatin(NewsEvent):
    templates = ["World's Largest %(animal)s Ever Recorded Found, Trapped, Killed, Sliced into Strips, then Eaten by Rural Evangelical Family in Alaska",]
    def gen(self):
        hl_tmpl = random.choice(self.templates)
        self.headline = apply_template_simple(hl_tmpl,'animal',animals)
        return self.headline

def debug(msg):
    if debugging:
        print msg

def capitalize_words(ln):
    debug('cap_words got: %s' % ln)
    pcs = ln.split(' ')
    def capitalize_word(w):
        if w[0].islower():
            return w.capitalize()
        else:
            return w
    pcs = map(capitalize_word,pcs)
    retval = ' '.join(pcs)
    debug('cap_words returning: %s' % retval)
    return retval

def read_file_as_lines(fname):
    with file(fname) as f:
        lns = f.readlines()
        lns = map(lambda ln: ln.strip(), lns)
        return lns

def dict_list_add(dicty, key, item):
    if key not in dicty:
        dicty[key] = []
    dicty[key].append(item)

def issubclass_strict(cls1, cls2):
    return issubclass(cls1,cls2) and cls1 is not cls2

def all_strict_subclasses_of(parent_class):
    subclasses = []
    class Klass: pass #TODO hackish but works, see use of Klass below
    for gk in globals():
        attr = globals()[gk]
        if type(attr) == type(Klass) and issubclass_strict(attr,parent_class):
            subclasses.append(attr)
    return subclasses

def prepare_data_category(fname, klass):
    data = []
    data_by_trait = {}
    values_for_prefix = {}
    lns = read_file_as_lines(fname)
    for ln in lns:
        debug('line: %s' % ln)
        fields = ln.split(',')
        fields = map(lambda x: x.strip(), fields)
        debug('fields: %s' % fields)
        name = fields[0]
        obj = klass(name)
        data.append(obj)
        if len(fields) >= 2:
            for trait in fields[1:]:
                if ':' in trait:
                    k,v = trait.split(':')
                    setattr(obj,k,v)
                    dict_list_add(values_for_prefix,k,v)
                dict_list_add(data_by_trait,trait,obj)
    return data, data_by_trait, values_for_prefix

def gen_news_events(tocks):
    events = {}
    hl_qty = 3 + random.randrange(5)
    headlines = []

    news_event_classes = all_strict_subclasses_of(NewsEvent)

    debug('news_event_classes: %s     %s' % (len(news_event_classes), news_event_classes))
    debug('tocks %s' % tocks)
    for t in range(tocks):
        debug('t %s' % t)
        for h in range(hl_qty):
            news_event_class = random.choice(news_event_classes)
            debug('news event class: %s' % news_event_class.__name__)
            event = news_event_class()
            headline = event.gen()
            if headline is None:
                continue
            if headline not in headlines:
                event.tock = t
                dict_list_add(events,event.tock,event)
    return events

def events_to_headlines(events):
    hlines = {}
    for tock in sorted(events.keys()):
        for event in events[tock]:
            dict_list_add(hlines,tock,event.headline)
    return hlines

def headlines(tocks = 2):
    events = gen_news_events(tocks)
    hlines = events_to_headlines(events)
    return hlines

def print_headlines(hlines):
    print '-' * 20
    print 'Top News'
    for tock in sorted(hlines.keys()):
        print '\nDay %s\n' % (tock + 1)
        for hline in hlines[tock]:
            print hline
    print '-' * 20

def main():
    events = gen_news_events(2)
    hlines = events_to_headlines(events)
    print_headlines(hlines)

debugging = False

nations = read_file_as_lines('data/nations')

stars = read_file_as_lines('data/stars')

animals = read_file_as_lines('data/animals')
animals = map(lambda ln: ln.capitalize(), animals)

homes = read_file_as_lines('data/homes')
homes = map(lambda ln: capitalize_words(ln.split(',')[0].strip()), homes)

jobs = read_file_as_lines('data/jobs')
jobs = map(lambda ln: capitalize_words(ln.split(',')[0].strip()), jobs)

markets = read_file_as_lines('data/markets')
markets = map(lambda ln: capitalize_words(ln), markets)

metals = read_file_as_lines('data/metals')
metals = map(lambda ln: ln.capitalize(), metals)

vehicles = read_file_as_lines('data/vehicles')
vehicles = map(lambda ln: capitalize_words(ln.split(',')[0].strip()), vehicles)

hurricane_names = ['Ike', 'Rita', 'Katrina', 'Enis']
hurricane_verbs = ['Threatens', 'Approaches', 'Slams']

cities, cities_by_trait, city_values_for_prefix = prepare_data_category('data/cities',City)

companies, companies_by_trait, company_values_for_prefix = prepare_data_category('data/companies',Company)

celebs, celebs_by_trait, celeb_values_for_prefix = prepare_data_category('data/celebs',Celeb)

sport_teams, sport_teams_by_trait, sport_values_for_prefix = prepare_data_category('data/teams',SportTeam)

diseases = read_file_as_lines('data/diseases')
diseases = map(capitalize_words,diseases)

if __name__ == '__main__':
    main()
