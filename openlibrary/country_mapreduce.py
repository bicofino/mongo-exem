#!/coding: utf-8

from mongo_util import conectar
from bson.code import Code
from pprint import pprint

db = conectar('openlibrary')

MAP = Code('''function () {
    pais = this.publish_country || "";
    pais.replace(/^|\s+$/g,"").toLowerCase();
    if (pais.length > 0) emit (pais, 1);
}''')

REDUCE = Code('''function (key, values) { 
    var total = 0;
    for (var i=0; i<values.length; i++) {
        total += 1;
    }
    return total;
}''')

db.editions.map_reduce(MAP, REDUCE, "country_stats")
res = [(int(r['value']), r['_id']) for r in db.country_stats.find()]
for qtd, pais in sorted(res, reverse=True):
    print '{qtd:6} {pais}'.format(**locals())
