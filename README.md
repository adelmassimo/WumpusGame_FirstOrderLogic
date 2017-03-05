# WumpusGame_FirstOrderLogic
1 Introduzione
L’esercizio svolto pone come obbiettivo la creazione di una base di conoscenza: tale conoscenza dovr ́a essere in grado di produrre inferenza utilizzando una tecnica di Backward Chaining.
Al fine di contestualizzare la conoscenza, mettendo in pratica i meccanismi implementati, useremo il mondo del Wumpus, all’interno del quale, un agente ibrido dovra ́ cercare di arrivare al goal.
Il mondo del Wumpus `e piuttosto semplice: ci sono delle buche (P), le quali causano una brezza (B) nelle caverne adiacenti, esiste un mostro, il Wumpus (W), che, come per le buche, provoca fetore (S) nelle caverne adiacenti, ed infine c’`e l’oro (G). Quest’ultimo sar ́a il nostro Goal.
2 Semplificazioni sul mondo del Wumpus
Il gioco originale prevede che l’agente sia munito di una singola freccia, scagli- abile in una delle direzioni nella speranza di colpire, e rimuovere dal mondo, il Wumpus. Nella versione originale anche l’oro produrrebbe uno scintillio nelle caverne adiacenti, in maniera del tutto analoga agli altri elementi. Per semplicita ́, in questa versione le regole sopracitate non verranno considerate: l’oro non emette scintillio e l’agente non ha frecce.
L’agente andr ́a quindi a muoversi all’interno del mondo fin’ora descritto; la modalita ́ di apprendimento di informazioni `e piuttosto intuitiva: ogni volta che l’agente si spostera ́ in una caverna inesplorata sara ́ soggetto a delle percezioni, volendo fare un esempio:
spostandosi nella caverna (2,1), l’agente potrebbe percepire la seguente formula:
S21∧B21∧¬G21∧¬P21∧¬W21
Ogni percezione di questo tipo verra ́ divisa nelle 5 formule atomiche e sal- vata nella Knowledge Base dell’agente. Questo per ́o non ci basta, serve che l’agente sia al corrente delle regole del mondo: il fatto che una buca produca una brezza nelle caverne adiacenti `e una regola. Il testo RN 2009 esprime queste regole atemporali nella forma:
B11 ⇐⇒ (P01∨P02∨P10∨P12) (1)
Dovendo usare un algoritmo di Backward, che come obbiettivo riceve P op- pure W, per verificare se una caverna `e sicura o meno, ho ritenuto che potesse essere piu` comodo usare una notazione diversa, come segue:
P11 ⇐⇒ (B01∨B02∨B10∨B12) (2) 1
In questo modo metto in evidenza P rispetto alle B. Volendo fare un esempio numerico:
Supponiamo di trovarci in un ambiente 4 x 4. Questo implica che ci saranno 16 regole atemporali per le buche. Se usiamo la notazione (1) avremo che una formula atomica Pxy comparir ́a al piu ́ in 4 assiomi. Avendo 16 cav- erne, negli assiomi dell’agente le formule atomiche che indicano P compari- ranno 44 volte, con una molteplicit ́a per la singola che varia tra 2 e 4.
Se invece usiamo (2) avremo che una stessa formula atomica P comparir ́a solamente una volta, quindi avremo 16 formule che contengono P.
`e chiaro che accade il contrario per le atomiche B, che indicano la brezza.
3 Rappresentazione della Conoscenza
La base di conoscenza si basa su una struttura piuttosto semplice, essa `e definita all’interno della classe knowledgeBase.py. Prima di definire meglio tale costrutto `e opportuno definire sintassi e semantica delle formule.
3.1 Rappresentazione delle Formule
La definizione della sintassi e della semantica avviene tutta all’interno del file proposition.py. Per semplicit ́a le formule trattate possono essere o Atomiche oppure Operatori binari, e questo implicha che, volendo avere un AND tra 3 formule A, B e C non potr ́o creare una formula del tipo: AND(A, B, C), dovremo bens ́ı utilizzare: AND(A, AND(B, C)).
3.2 Knowledge Base
Per la rappresentazione della conoscenza ho utilizzato un’unica classe: Knowl- edgeBase. Quest’ultima `e composta da una lista clauses, il vero e proprio nucleo della conoscenza, e dai seguenti metodi:
• TELL:halaclassicafunzionediaggiungereproposizioniallaconoscenza. • ASK: riceve in ingresso una proposizione e ritorna un valore booleano
a seconda della veridicita ́ di tale proposizione nel contesto di clauses.
3.3 Backward Chaining
L’algoritmo richiesto per la risoluzione delle query, come da titolo, `e Back- ward chaining. Tale algoritmo opera partendo dal goal per poi risalire alle
2
1 2 3 4 5 6 7
8 9
10
11
12
13
14
15
16
17
18
19
condizioni necessarie. In questo contesto le interrogazioni saranno quelle che porr ́a l’agente alla propria conoscenza per evincere se una caverna `e sicura o meno: in questo caso i goal saranno “not Pxy” e “not Wxy”, e se l’algoritmo ritornera ́ True in entrambi i casi, sicuramente [x, y] sara ́ sicura. Al contrario se almeno una delle due interrogazioni risulta False significa che non ci sono sufficienti presupposti per determinare che sia sicura. Questo non implica che non lo sia.
L’algoritmo `e riportato di seguito.
def backwardChaining(self, q :Formula):
if str(q) in self.clauses.stringList():
return True
elif isinstance(q, Not):
return not self.backwardChaining(q.child)
elif isinstance(q, And):
return self.backwardChaining(q.leftOp) and
self.backwardChaining(q.rightOp)
elif isinstance(q, Or):
return self.backwardChaining(q.leftOp) or
self.backwardChaining(q.rightOp)
for arg in self.clauses:
if isinstance(arg, Iff):
if str(arg.leftOp) == str(q):
return self.backwardChaining(arg.rightOp)
elif str(arg.rightOp) == str(q):
return self.backwardChaining(arg.leftOp)
elif isinstance(arg, Implies):
if str(arg.leftOp) == str(q):
return self.backwardChaining(arg.rightOp)
return False
E` un algoritmo piuttosto semplice ed opera in maniera ricorsiva, fino a ri- condursi a formule atomiche.
4 L’agente ed il mondo del Wumpus
L’agente implementato utilizza una strategia definibile ibrida, in quanto non opera puramente su base logico-proposizionale, ma bens ́ı si appoggia ad un algoritmo di esplorazione: la ricerca in ampiezza.
In definitiva, l’agente interroga la propria conoscenza per scoprire se una cav- erna `e sicura o meno, mentre per spostarsi all’interno del mondo (e tenere conto della propria frontiera) utilizza l’algorimo BFS. Da notare che in questo
3

modo la frontiera aumenta in maniera costante e impedisce all’agente di pas- sare da una cella X ad una Y non adiacenti. Questo perch ́e all’agente `e consentito solamente spostarsi sulla frontiera, e ad ogni passo quest’ultima si espande. A grandi linee, l’algoritmo di gioco opera come segue:
function Play:
move Agent in [0,0];
while isAlive AND NOT win do
get Perceptions from currentRoom; update safeRooms[];
if safeRoom[] is not empty then
move to a safe room;
update frontier[];
current section becomes this one;
else
if frontier[] is not empty then
move to a random room of frontier[];
else
isAlive = False;
end end
end
Algorithm 1: Funzione play() in agent.py. 5 Conclusioni
Bisogna premettere che essendo il mondo creato casualmente non `e detto che ammetta sempre soluzione: questo si verifica con una cadenza di circa 3 volte su 10 (nel caso di un mondo 4x4 con 3 buche), quindi l’agente si `e comportato bene 238 volte su 1000.
Potrebbe non sembrare un gran risultato, questo `e dovuto al fatto che im- plementa una tecnica che in caso di indecisione “lancia una monetina”, e questo, su una frontiera sempre piu ́ grande, porta ad una maggiore prob- abilita ́ di sbagliare. Per ovviare a questo problema si potrebbe pensare di procedere utilizzando un approccio probabilistico come suggerito in RN. Per quesrtioni di praticit ́a non ho implementato anche questo tipo di strategia.
4
