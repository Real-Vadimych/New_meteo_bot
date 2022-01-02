import re

test = """SPMI 30 Dec 2021 02:32 UTC
----------------------------------------
TAF USII 300200Z 3003/3012 15003G08MPS 8000 BKN011
TXM15/3011Z TNM22/3004Z TEMPO 3003/3006 1000 BR BKN003
BECMG 3006/3008 BKN016=

FTUSII NIL=
WSUSTV NIL=
----------------------------------------"""

# p = re.compile('----------------------------------------((\n.*)+=)\n\n')
p = re.compile('(?s)-{40}(.*?)=', flags=re.DOTALL)

result = p.findall(test)[0].replace('\n', '', 1)

print(result)
