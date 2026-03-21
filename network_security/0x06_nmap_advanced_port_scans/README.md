Giriş

Bu layihədə biz Nmap vasitəsilə advanced (inkişaf etmiş) port scan üsullarını öyrənirik.
Məqsədimiz müxtəlif scan növlərinin necə işlədiyini başa düşmək və onların real şəbəkələrdə necə davrandığını görməkdir.

Burada sadəcə komanda əzbərləmirik — məntiqini anlayırıq.

🎯 Məqsəd
Müxtəlif Nmap scan növlərini öyrənmək
Stealth (gizli) scan-lərin necə işlədiyini başa düşmək
Firewall və IDS/IPS sistemlərinin bu scan-lərə reaksiyasını analiz etmək
Real lab mühitində praktika etmək
🛠️ İstifadə olunan alətlər
Nmap
Linux (Kali Linux və ya digər distro)
Virtual maşınlar (lab mühiti üçün)
🔍 Əsas Scan Növləri
1. SYN Scan (-sS)
Yarım (half-open) connection qurur
Tam TCP handshake etmir
Nisbətən stealth sayılır

👉 Ən çox istifadə olunan scan növlərindən biridir

2. NULL Scan (-sN)
Heç bir TCP flag istifadə etmir
Open port → cavab yoxdur
Closed port → RST

👉 Sadə firewall-ları bypass edə bilər

3. FIN Scan (-sF)
Yalnız FIN flag istifadə edir
NULL scan-a bənzər davranır

4. Xmas Scan (-sX)
FIN + PSH + URG flag-ləri istifadə edir
Paket “Christmas tree” kimi görünür 🎄

👉 Qeyri-adi olduğu üçün bəzi sistemləri çaşdıra bilər

5. Maimon Scan (-sM)
FIN + ACK flag istifadə edir
Daha çox köhnə sistemlərdə effektivdir
6. Fragmented Scan (-f)
Paketləri hissələrə bölür
Məqsəd: firewall-u bypass etmək
🕵️ Stealth vs Aggressive
Stealth Scan
Gizli işləyir
Az trafik yaradır
Daha yavaşdır
Detection riski azdır
Aggressive Scan (-A)
Çox məlumat toplayır
Sürətlidir
Asanlıqla detect olunur
🛡️ Firewall və Detection

Müasir firewall-lar:

Stateful inspection istifadə edir
Qeyri-adi TCP flag-ləri aşkar edir
Stealth scan-ləri belə görə bilir

⚠️ Vacib Qeyd

Bu biliklər:

Yalnız tədris və lab mühiti üçün istifadə olunmalıdır
İcazəsiz sistemlərə scan etmək qanunsuzdur
💡 Nəticə

Bu mövzu bizə öyrədir ki:

Hər scan növünün öz məqsədi var
“Stealth” hər zaman görünməz demək deyil
Müasir təhlükəsizlik sistemləri çox inkişaf edib
