# MDVA Agency: progetto generale dell'applicazione

> Documento da allegare a un'altra chat AI per finalizzare la piattaforma.
> Descrive cosa è l'app oggi, com'è costruita, come funziona ogni parte e cosa resta da fare.
> Versione analizzata: pagina "MDVA Agency" su claude.ai (aggiornata il 16/11/2026), file unico HTML di circa 600 KB e 5.850 righe.

---

## 1. In una frase

MDVA Agency è una **sede virtuale per un'agenzia di marketing digitale**. Il titolare apre la sede ogni mattina e una squadra di **28 professionisti AI**, divisi in **14 reparti**, organizza la giornata, lavora sui clienti, consegna lavoro finito e chiede approvazione al titolare per ogni decisione importante (pubblicare, spendere, contattare, pagare).

## 2. Contesto del business

- **Titolare**: gestisce un'agenzia di video, social e ads per negozi e aziende. Priorità alla **Campania**; fuori regione si valuta caso per caso.
- **Come lavora oggi**: il titolare gira i contenuti dal cliente, il team monta, pubblica e gestisce le ads.
- **Brand proprio**: abbigliamento streetwear (felpe), venduto online su **Shopify** (B2C) e ai negozi (B2B). Le spedizioni le fa il titolare.
- **Budget indicativo**: 1.000–5.000 € al mese.
- **Clienti collegati** (da altri progetti dello stesso titolare): EMME Clothes (brand di abbigliamento), Punto Eurobet, il barbiere "Il Protagonista", NO MERCY.
- **Lingua**: tutta l'app e tutte le risposte dello staff sono in **italiano semplice**: prima la conclusione, poi i dettagli.

## 3. Obiettivi del prodotto

1. Dare al titolare una squadra completa (strategia, social, video, grafica, ads, e-commerce, logistica, finanza, legale, lead B2B) senza assumere nessuno.
2. Trasformare un'idea in **lavoro consegnato e pronto da usare**: copioni, piani editoriali, grafiche PNG, pagine prodotto, piani ads, report.
3. Tenere il titolare al centro delle decisioni senza farlo diventare un collo di bottiglia: lo staff decide da solo sul quotidiano e chiede su soldi, pubblicazioni, contratti e reputazione.
4. **Niente di inventato**: nessun numero, risultato, recensione o cliente finto. Se un dato manca, lo staff lo dice e lo chiede.
5. Funzionare bene **da telefono** (il titolare lo usa soprattutto da iPhone) e anche da Mac.

---

## 4. Architettura tecnica attuale

| Aspetto | Situazione |
|---|---|
| Forma | **Un solo file HTML** con CSS e JavaScript inline (vanilla JS, nessun framework) |
| Hosting | Artifact privato di claude.ai, fissato nella barra laterale |
| 3D | `three.js r128` da cdnjs per la sede 3D; esiste anche una pianta SVG 2D di riserva |
| Font | Google Fonts: Schibsted Grotesk, IBM Plex Sans/Mono, Sora, Inter; lo stile finale sovrascrive con **Bodoni Moda + Manrope** |
| AI | Runtime di Claude dentro la pagina: `claude.use("sample")` → `sample.json(prompt, {modelTier:"complex"})`. Ogni chiamata chiede **solo JSON**; se il JSON non è valido riprova una volta |
| Database | `claude.use("db")` + `claude.use("user")`: un documento per chiave nella collezione `data/users/<uid>` (dati per utente). Se il db manca, ripiega su `localStorage` con prefisso `qg-` |
| File | `claude.use("assets")` → `assets.upload(file)` per foto, video e reference. Senza assets usa `URL.createObjectURL` (temporaneo) |
| Download | `claude.use("downloads")` → `downloads.save(...)` per scaricare grafiche e documenti |
| Shopify | `claude.use("mcp")` → `mcp.callTool(...)` sul server MCP **Shopify**, in **sola lettura**. Strumenti dichiarati: `get-shop-info`, `list-orders`, `run-analytics-query`, `search_products`, `get-inventory-levels` |
| Voce in uscita | Web Speech API (`speechSynthesis`): voce italiana diversa per ogni persona (femminile/maschile, tono e velocità propri), preferendo le voci Premium/Migliorate |
| Voce in entrata | Dettatura col microfono (🎙) e, in alternativa, dettatura della tastiera; opzione "invia da solo dopo 2 secondi di pausa" |
| Modalità locale Mac | Se `window.MVDA_LOCALE` è attivo, la pagina parla con un server locale: `/api/stato`, `/api/voce` (voci **Piper**, più umane), `/api/video` (montaggio reale con **ffmpeg**) |
| Capacità dichiarate dell'artifact | `assets`, `db`, `downloads`, `mcp` (Shopify), `sample` (con immagini), `user` |

**Limite importante**: senza il runtime di Claude (pagina aperta fuori da claude.ai) lo staff non lavora: compare "Apri questa pagina dal link di Claude per far lavorare lo staff".

---

## 5. La squadra: 14 reparti, 28 persone

Ogni persona ha: nome, genere, reparto, ruolo, formazione, anni di esperienza, specialità, responsabilità, competenze extra, strumenti, carattere, KPI del reparto, voce propria, colore e avatar. Il titolare può **rinominare** chiunque (pannello "Personale").

| Reparto | Persone (ruolo) | KPI del reparto |
|---|---|---|
| Direzione operativa | **Franco**: Direttore operativo (COO), coordina tutto · **Alessandro**: Strategia e sviluppo | obiettivi raggiunti, progetti in tempo, scostamento budget |
| Strategia di brand | **Elena**: Senior Brand Strategist, scrive i copioni · **Martina**: Ricerca consumatori e mercato | posizionamento, ricerca, coerenza |
| Marketing e crescita | **Davide**: CMO · **Sofia**: Growth Marketing Manager | ricavi incrementali, CAC, retention, conversioni |
| Social e community | **Giulia**: Social Media Manager senior, propone ogni giorno IL video da girare · **Chiara**: Community & Influencer Manager | crescita qualificata, engagement, traffico, qualità |
| Foto, shooting e video | **Luca**: Direttore creativo, grafiche, mockup e revisione video · **Sara**: Producer e video editor | puntualità, varianti, performance |
| Pubblicità | **Marco**: Head of Performance Marketing · **Federico**: Media Buyer | CPA, ROAS, margine dopo ads, tracking |
| E-commerce, web e CRO | **Valentina**: E-commerce Manager · **Matteo**: Web Developer / CRO (Liquid Shopify) | conversione, AOV, velocità, errori checkout |
| Ricerca prodotto e sourcing | **Giorgia**: Product Research · **Andrea**: Fornitori e campioni | margini, qualità, tempi, difetti |
| Logistica e ordini | **Roberto**: Supply Chain · **Simone**: Magazzino e spedizioni | inventario, evasione, errori, resi |
| Amministrazione e finanza | **Paolo**: Amministrazione e finanza · **Laura**: Controller | report puntuali, previsioni, liquidità, marginalità |
| AI, dati e automazione | **Nicola**: AI & Data Lead, "verificatore di realtà" · **Irene**: Automation Engineer | ore risparmiate, affidabilità, errori, adozione |
| Persone, legale e conformità | **Francesca**: HR · **Stefano**: Legal & Compliance | selezione, retention, formazione, conformità |
| Lead generation B2B | **Marta**: Lead Generation Manager · **Gabriele**: Ricerca negozi e primo contatto | lead pertinenti, contatti verificati, risposte, chiamate accettate |
| CRM e qualificazione | **Elisa**: CRM & Sales Ops · **Lorenzo**: Lead Qualifier | completezza dati, duplicati, passaggi al titolare, follow-up |

Ogni persona ha anche una **scheda operativa** (`CARD`): da chi riceve il lavoro, a chi lo passa, a chi chiede aiuto, quali passaggi della catena contenuti gestisce e le sue regole personali (es. Marco: "nessuna spesa senza ok del titolare"; Paolo: "l'utile netto non è vendite meno pubblicità").

Esistono anche 4 **reparti dei contenuti** trasversali: Short (Reel/TikTok), Video lunghi (YouTube/VSL), Generazione AI, Caption, pubblicazione e automazioni.

---

## 6. Le regole comuni (il "cervello" dello staff)

Ogni chiamata AI riceve un contesto composto da: metodo di lavoro + regole comuni + profilo e scheda della persona + skill + formazione + dati aziendali + reparto + cliente + memoria del cliente + diario della squadra + decisioni approvate.

**Regole comuni MDVA (sopra ogni altra indicazione)**
1. **Niente di inventato**: mai dati, numeri, risultati, recensioni, fonti o clienti finti. Se manca un dato si scrive «dato mancante» e chi può fornirlo. Ogni numero dice da dove viene.
2. **Il titolare decide**: pubblicare, spendere, pagare, rimborsare, firmare, scrivere a clienti o fornitori, cancellare → sempre conferma. Nessuna assunzione o freelance da soli.
3. **Catena contenuti in 12 passaggi**: un passaggio si sblocca solo quando il precedente è finito e approvato. Ogni modifica crea una nuova versione. "Pubblicato" solo con conferma reale (link).
4. **Clienti separati**: dati e idee di un cliente non finiscono mai nel lavoro di un altro. Si lavora solo sui servizi attivati per quel cliente.
5. **Conti onesti**: utile netto = ricavi − costo del venduto − spedizioni − commissioni − resi − pubblicità − costi fissi − tasse.
6. **Livelli di competenza 0–4**: salgono solo con lavori consegnati e approvati.
7. **Privacy**: niente sorveglianza, GDPR, mai password o dati di pagamento nei messaggi.
8. **Italiano semplice**, prima la conclusione.

**Metodo di problem solving** (8 passi): definisci il problema → raccogli dati → separa fatti, ipotesi e opinioni → confronta soluzioni → confrontati col collega → raccomanda → esegui ciò che è autorizzato → misura e documenta.

**Ogni consegna termina con**: «Perché porta risultati», «Come lo misuriamo», «Prossimo passo», «Passo a…».

**Deleghe**
- *Decidono da soli*: attività quotidiane, test autorizzati entro budget, calendario editoriale, ottimizzazioni operative, compiti interni, acquisti ricorrenti entro soglia.
- *Chiedono al titolare*: assunzioni, spese oltre soglia, debiti e impegni pluriennali, cambi di prezzo o posizionamento, mercati con rischi normativi, contratti rilevanti, reputazione e liquidità.

---

## 7. Le sezioni dell'app (navigazione)

Navigazione: barra laterale fissa su desktop (≥1100 px), barra in basso su telefono (≤760 px) con le voci principali **Sede** e **Parla** e il pulsante **Altro** per il resto. In alto: "+ Nuovo lavoro", "Voce", "Personale", orologio.

### 7.1 Sede (schermata iniziale)
- Saluto ("Buongiorno, capo") e riepilogo; pulsanti **✋ Sono presente** e **Organizza la giornata**; filtro per reparto e per cliente.
- **Sede 3D** (three.js): open space illustrato con le stanze dei reparti, scrivanie e persone sedute. Tocchi una stanza per entrare, trascini per muoverti, zoom +/−. Un pannello laterale (dal basso su telefono) mostra il reparto. In riserva c'è la pianta SVG 2D vista dall'alto.
- Stato di ogni persona con colori e animazioni: *A casa*, *Al lavoro*, *In attesa/In coda*, *Ha finito*, *Ha un problema*.
- Striscia **In diretta** con cosa sta facendo lo staff in tempo reale; indicatori (KPI); griglia della squadra su telefono.
- Pannelli: **Oggi tocca a te**, **Rapporto del direttore**, **Da approvare**, **Registro della sede**; vassoio "Tocca a te".
- **Flusso della giornata** (`openDay`):
  1. Il titolare preme "Sono presente" (eventuale nota del mattino, es. "oggi priorità al cliente nuovo, 50 € di ads").
  2. Franco legge incarichi attivi, lavori rimasti da ieri e la nota, poi crea **fino a 14 compiti** (uno per persona) distribuiti sui clienti. Per il brand del titolare, il social propone sempre il video da girare oggi.
  3. Le persone "entrano" una alla volta e si siedono.
  4. Ognuno esegue il compito (`runTask`), anche in catena (un compito può partire dal lavoro consegnato da un collega).
  5. Revisione finale, rapporto del direttore e lista "da fare tu" per il titolare.
  6. Se un lavoro è bloccato, compare una chiamata "ci servi" in cima alla pagina.

### 7.2 Parla
Chat unica con lo staff ("risponde l'esperto giusto"). Scelta del cliente, selezione di un esperto (Direttore, Strategia, Foto, Video, Social, Sponsorizzate, Contabilità…), suggerimenti pronti, allegati foto/video, dettatura, voce on/off, **📞 Call** generale con tutta la squadra sul cliente scelto. Da qui lo staff può anche **mettersi al lavoro** (crea compiti) o avviare la **catena di produzione per un cliente nuovo** (strategia → copioni → shooting → piano video → piano social → piano ads, con dipendenze).

### 7.3 Scrivania (home)
"Chiedi alla squadra": casella di comando (es. "Preparami 3 idee di Reel per la felpa nera"), il direttore assegna. Poi: scorciatoie, ultime consegne, numeri del mese, cose da fare con spunta, prossimi contenuti, la squadra adesso.

### 7.4 Consegne
Archivio di tutto il lavoro consegnato. Filtri per testo, persona, cliente e stato (*Da vedere*, *Approvate*, *In modifica*, *Preferite*). Ogni consegna si apre in un pannello: **Approva**, **Preferita**, **Copia**, **Scarica**, **Elimina**, oppure **chiedi una modifica** a voce o per iscritto (crea una nuova versione). Dalle correzioni Franco **ricava una regola** e la salva per il futuro (`learnFromFix`).

### 7.5 Calendario dei contenuti
Vista settimanale (7 giorni, una colonna su telefono), filtro cliente, "Giulia, pianifica la settimana", aggiunta manuale. Ogni contenuto ha: giorno, ora, canale (Instagram/TikTok/Entrambi), formato (Reel, Carosello, Storia, Post, Live), titolo, cosa girare, didascalia, hashtag, stato (*Da fare*, *Girato*, *Pubblicato*) e **link del post, obbligatorio per segnarlo pubblicato**. Un contenuto pubblicato non si sposta.

### 7.6 Catena contenuti
Pipeline dal copione alla pubblicazione, con fasi bloccanti:

| # | Fase | Chi |
|---|---|---|
| 1 | Copione in scrittura | Elena (automatico) |
| 2 | Copione da approvare | Titolare |
| 3 | Da girare | Titolare (carica le clip o un link) |
| 4 | In montaggio | Sara (automatico) |
| 5 | Controllo qualità | Luca (automatico, non può approvare un lavoro suo) |
| 6 | Montaggio da approvare | Titolare |
| 7 | Didascalia in preparazione | Giulia (automatico) |
| 8 | Pacchetto da approvare | Titolare |
| 9 | Approvato · da pubblicare | Titolare |
| 10 | Pubblicato | Solo con link reale Instagram/TikTok/Facebook/YouTube |

Dopo la pubblicazione (passaggi 11–12 della regola): raccolta dei numeri e lezioni della strategist per i contenuti successivi. Ogni elemento tiene lo **storico delle fasi** e fino a **6 versioni**; badge con quanti elementi aspettano il titolare.
**Revisione video**: player con versioni, note al secondo esatto, disegno sopra il fotogramma e immagini. In modalità Mac, Sara decide i tagli e **ffmpeg monta davvero il file**, anche con grafiche animate.

### 7.7 Riunioni e call
- **Sala riunioni**: argomento, cliente, partecipanti selezionabili. Parla solo chi ha qualcosa di utile da dire; nessuno ripete cose già dette. Verbale e note automatiche.
- **Riunione di benvenuto** (onboarding): il primo giorno il titolare presenta il brand, lo staff fa domande e compila da solo la scheda del brand e un piano iniziale.
- **Call vocale** a schermo intero, stile videochiamata: riquadri dei partecipanti, chi parla si illumina, sottotitoli, timer, allegati, invio automatico dopo una pausa.
- **Telefonata singola**: dal pannello di una persona, "📞 Chiama".

### 7.8 Lavori per cliente
Scegli il cliente e vedi chi ci lavora, i lavori di oggi, clip e montaggi, consegne e pubblicazioni programmate. Pulsanti: "Oggi lavoriamo per questo cliente", "Presenta il cliente allo staff", "Scegli tu la squadra".
**Carica le clip girate** (video fino a 20 MB l'una, oppure link a Drive/WeTransfer/iCloud) con obiettivo, messaggio, invito all'azione, piattaforma, data e note. Stati della clip: *Ricevuta → In montaggio → Montaggio pronto → Programmata → Pubblicata*. Promemoria di pubblicazione.

### 7.9 Negozio Shopify (sola lettura)
Dati reali dal negozio: indicatori, ultimi ordini con stato di pagamento e spedizione, prodotti e scorte (sotto 5 pezzi = sotto scorta). Quattro lavori pronti dello staff:
- **Valentina**: analizza il negozio e propone 5 azioni in ordine di impatto.
- **Roberto**: scorte e riordini, con quantità motivate (solo proposta).
- **Simone**: ordini da spedire e lista di preparazione dei pacchi.
- **Paolo**: vendite a 1, 7 e 30 giorni, distinguendo vendite, incassi e utile.
L'app **non modifica mai** prodotti, prezzi, scorte o ordini.

### 7.10 CRM lead B2B
- **Profilo del cliente ideale** (lo può scrivere Marta).
- Kanban con fasi: *Da verificare → Contattato → Interessato → Da chiamare → Chiamato → Cliente* / *Non interessato*.
- Scheda lead: azienda, città, sito e social, referente, settore, perché è pertinente, telefono (solo se pubblico), fonte e data, interesse, fascia oraria, prossimo passo, consenso e base giuridica.
- Azioni: **Gabriele** scrive il primo messaggio · **Lorenzo** qualifica (caldo/tiepido/non idoneo) · "Passa a me per la telefonata" · registra l'esito · "È diventato cliente".
- **L'app non contatta nessuno da sola**: lo staff scrive, il titolare invia. Niente scraping vietato, solo dati pubblici e pertinenti.

### 7.11 Organigramma
Dati aziendali modificabili (titolare, modello di vendita, agenzia e zona, paese, città, settore, piattaforme, logistica, budget, strumenti): lo staff usa solo questi e chiede quello che manca. Deleghe. Reparti con persone, budget mensile, soglia di spesa senza approvazione e obiettivo trimestrale. Toccando una persona si vedono e modificano **istruzioni e skill**.

### 7.12 Registro
Cinque sezioni: **Decisioni**, **Rischi**, **Problemi**, **Procedure** (precaricate), **Report** direzionali generati su N giorni (`makeReport`).

### 7.13 Progetti di squadra
Obiettivo con un numero ("60 ordini entro il 15 dicembre con 600 € di ads"), cliente e scadenza. Il direttore pianifica chi fa cosa e in che ordine; ognuno parte dal lavoro di chi viene prima; alla fine arriva un **pacchetto completo**. Progetti pronti: Crescere in tutta Italia, Lancio delle felpe, Video virali TikTok, Ads che convertono, Black Friday e Natale, Avvio cliente nuovo.

### 7.14 Studio creativo
Input: cliente, prodotto, prezzo, formato (Post 4:5 1080×1350, Storia 9:16 1080×1920, Quadrato 1080×1080), dettagli, tipo di capo (felpa con cappuccio o girocollo), logo PNG, fino a 6 foto.
- **🎨 Crea 3 grafiche ads** (Luca): tre grafiche disegnate su canvas, scaricabili in PNG.
- **🛍 Pagina prodotto** (Elena e Luca): titolo, descrizione che vende, punti chiave, vestibilità, cura, FAQ, testi SEO pronti per Shopify.
- **🎬 Idee video** (Sara e Giulia): tre video con gancio, scene, testo a schermo, audio e riferimenti.
- **🧵 Mockup e colori** (Luca): tre varianti di colore e tessuto con la stampa posizionata, fronte e retro della felpa disegnati su canvas, scheda tecnica per il fornitore e prompt per foto realistiche con l'AI.
Luca può anche disegnare grafiche in SVG (sanificato) e applicarle sul capo.

### 7.15 Risultati
Per cliente: obiettivi del mese e numeri settimanali inseriti a mano (ordini, fatturato, scontrino medio, spesa ads, ROAS, conversione, follower IG e TikTok), storico, "Analizza con la squadra" (semaforo e variazioni). I numeri si inseriscono a mano finché gli account non sono collegati.

### 7.16 Clienti e incarichi
Lista clienti (il primo è sempre il brand del titolare, tipo `mio`) con scheda del brand in 12 campi: cosa vende, target, identità, tono di voce, cosa non dice mai, temi fissi, stile visivo, riferimenti, canali e numeri, costi/compenso, obiettivi, pagine e link. Servizi attivabili SÌ/NO: Strategia, Gestione social, Video, Shooting e foto, Sponsorizzate. Incarichi per persona e cliente, modificabili. C'è anche un pulsante per far compilare la scheda all'AI (`brandAi`).

### 7.17 Comunicazioni
Messaggio a tutto lo staff ("ho preso un nuovo cliente…"), anche creando un nuovo cliente al volo. Rispondono solo i reparti interessati: confermano, accettano e si creano l'incarico.

### 7.18 Pannelli trasversali
- **Pannello persona**: profilo e CV, compiti, chat 1-a-1, modalità "Parla" o "Dai un compito", allegati, dettatura, chiamata.
- **Cervello condiviso** (curato da Franco): regole, note di revisione, reference studiate (foto, video e link analizzati da `studyRef`), lavori approvati, attività degli ultimi 14 giorni.
- **Da approvare**: tutto ciò che aspetta il titolare, in un unico posto.
- **Personale**: rinomina le persone.
- **Prova le voci**: chi parla con quale voce, attivazione di Piper sul Mac.
- **Ricomincia da zero**: reset completo dei dati.

---

## 8. Memoria e apprendimento

| Livello | Cosa contiene | Come resta corta |
|---|---|---|
| **Memoria per cliente** (`mem-<id>`) | tutto ciò che accade su un cliente: messaggi, consegne, correzioni, approvazioni | Franco la riassume periodicamente (`memCompress`) |
| **Diario della squadra** (`diario`) | memoria continua di tutte le conversazioni | riassunto automatico (`diaryCompress`) |
| **Formazione** (`formazione`) | come vuole le cose il titolare, persona per persona | riassunto per persona |
| **Skill** (`skills`) | metodi di lavoro modificabili dal titolare (ganci, metodo WATCH per i copioni, didascalie sotto 125 caratteri, montaggio pensato senza audio, ecc.) | versione `_v:2` con migrazione |
| **Lezioni** (`lezioni`) | regole ricavate dalle correzioni | — |
| **Decisioni approvate** | ultime 12 decisioni valide, per cliente | — |
| **Reference** (`reference`) | foto, video e link studiati | — |

---

## 9. Modello dati (chiavi salvate)

Tutte le chiavi stanno in `data/users/<uid>/<chiave>`; senza db stanno in `localStorage["qg-<chiave>"]`.

```
clients      {items:[{id, nome, tipo:"mio"|..., colore, scheda:{12 campi}, servizi, since}]}
incarichi    {items:[{id, cliente, chi, titolo, descrizione, stato:"attivo", since}]}
day-YYYY-MM-DD {date, openedAt, arrivals:{id:ts}, piano:{saluto,focus}, tasks:[{id,chi,cliente,titolo,istruzioni,stato:"coda|lavoro|fatto|bloccato",consegna,problema,dopo:[ids]}], report, decisioni, log, nota}
meta         {lastDay}
catena       {items:[{id, cliente, piattaforma, formato, obiettivo, idea, fase, storia:[...], versioni copione/montaggio/didascalia (max 6), clip, link}]}
clip         {items:[{id, cliente, file/link, obiettivo, messaggio, cta, piattaforma, data, note, stato}]}
calendario   {items:[{id, cliente, data, ora, canale, formato, titolo, idea, didascalia, hashtag, stato, link}]}
archivio     {items:[{id, chi, cliente, titolo, testo, fonte, at, stato:"nuovo|approvato|rivedere", preferito}]}
crm          {icp, items:[{id, fase, campi lead..., log:[interazioni]}]}
progetti, risultati, studio, todo, decisions, files, chats, comms, meeting, calls,
names, azienda, registro, sala, benvenuto, formazione, skills, lezioni, reference, diario, mem-<clienteId>, brand (vecchia versione)
```

---

## 10. Design

- **Stile attivo**: "luxury" scuro unico: fondo `#0A0A0C`, superfici `#131316`, testo `#F2EEE6`, **oro** `#C9A961` / `#E6CB8E`, pulsanti principali con gradiente oro, titoli in **Bodoni Moda**, testo in **Manrope**, card con angoli da 16 px e ombre profonde.
- Colori di stato: al lavoro (oro), in attesa (blu `#93AEDC`), fatto (verde `#84BE94`), problema (rosso `#E38672`).
- Ogni reparto ha un suo colore e un'icona (📋 🧭 📈 📱 🎨 🎯 🛒 🔍 📦 📊 🤖 ⚖️).
- Mobile first: barra in basso, finestre a schermo intero su telefono, aree sicure iPhone, pulsanti a misura di pollice, rispetto di `prefers-reduced-motion`.
- **Brand kit MDVA separato** (per i contenuti Instagram dell'agenzia): nero `#0A0A0A`, **rosso MDVA `#E3141F`**, bianco `#F5F3F3`, grigio `#9C9496`; font Montserrat (titoli) e Inter (testo); slide 1080×1350 con parole chiave in rosso; ultima slide "Pronto a fare il prossimo passo? Scrivici in DM"; niente emoji nelle grafiche.
  → **Da decidere**: l'app usa l'oro, il brand kit il rosso. Conviene allineare l'app al brand kit o tenere i due stili distinti di proposito.

---

## 11. Problemi noti e incoerenze da sistemare

1. **Nome**: nel codice compaiono sia "MDVA" sia "MVDA" (`REGOLE_MVDA`, `MVDA_LOCALE`). Va scelto uno solo.
2. **Commenti superati**: "12 reparti, 2 professionisti ciascuno" e "organico ampliato a 24", mentre oggi sono 14 reparti e 28 persone.
3. **File unico di quasi 600 KB**, con CSS stratificato (v7, v11, v12, luxury…) e regole che si sovrascrivono con `!important`: difficile da mantenere.
4. **Due motori della sede** (SVG 2D e three.js 3D) da mantenere in parallelo.
5. **Costo e tempi AI**: aprire la giornata lancia 14+ chiamate `complex` in sequenza; non ci sono limiti di spesa né una coda visibile.
6. **Dati per utente**: il db è per singolo utente, quindi non c'è un vero lavoro di squadra tra più persone umane.
7. **Numeri social e ads inseriti a mano**: mancano i collegamenti a Instagram, TikTok e Meta Ads.
8. **File senza assets**: con `createObjectURL` le clip si perdono al ricaricamento.
9. **Voce**: la qualità dipende dalle voci installate sul dispositivo; Piper e ffmpeg funzionano solo in modalità Mac locale.
10. **Nessun test automatico** e nessuna gestione delle versioni del codice.

---

## 12. Cosa serve per finalizzarla (proposta di roadmap)

**Fase 1: pulizia (senza cambiare funzioni)**
- Nome unico "MDVA Agency" ovunque; aggiornare i commenti.
- Dividere il file in moduli: `staff.js` (dati), `prompts.js` (regole e contesto), `store.js` (salvataggio), `ai.js`, `ui/<sezione>.js`, `styles/`.
- Unificare il CSS in un solo sistema di token (decidere oro o rosso MDVA).
- Tenere un solo motore della sede (3D con fallback statico leggero).

**Fase 2: affidabilità**
- Coda delle chiamate AI con limite di parallelismo, nuovi tentativi, stato visibile e tetto giornaliero.
- Salvataggio file sempre persistente; avviso quando un file è solo temporaneo.
- Migrazioni versionate dei dati (`_v`) per ogni chiave.
- Esportazione e importazione di backup in JSON.

**Fase 3: integrazioni reali**
- Instagram/Facebook (Graph API) e TikTok per i numeri e per verificare il link "Pubblicato".
- Meta Ads e TikTok Ads in sola lettura per ROAS e CPA reali.
- Shopify: aggiungere costi dei prodotti per calcolare il margine vero.
- Klaviyo per email e flussi (già disponibile come connettore).

**Fase 4: prodotto**
- Login vero e più utenti umani (titolare più eventuali collaboratori) con permessi.
- Portale cliente in sola lettura (calendario, consegne approvate, report mensile).
- Report mensile PDF per ogni cliente.
- Versione app installabile (PWA) per iPhone.

**Se si vuole uscire da claude.ai** (app indipendente): servono un backend (es. Next.js + Supabase/Postgres), chiamate dirette alle API di Anthropic al posto di `sample.json` (modello consigliato: la famiglia Claude più recente, con un livello più economico per i compiti semplici), uno storage file (S3 o Supabase Storage), autenticazione, e un server per Shopify Admin API (in sola lettura), ffmpeg e TTS.

---

## 13. Istruzioni per l'AI che riceve questo documento

- Mantieni **tutte le regole della sezione 6**: sono il cuore del prodotto (niente di inventato, il titolare decide, catena bloccante, clienti separati, conti onesti).
- Interfaccia e testi **solo in italiano semplice**, pensati prima di tutto per il telefono.
- Nessuna azione verso l'esterno senza conferma: l'app propone, il titolare invia, pubblica e spende.
- Shopify resta in **sola lettura**, salvo decisione esplicita del titolare.
- Prima di riscrivere, chiedi al titolare: (1) restare dentro claude.ai o diventare un'app indipendente? (2) oro o rosso MDVA? (3) quali integrazioni servono per prime? (4) userà l'app da solo o con collaboratori?
- Il file sorgente attuale (HTML completo) può essere fornito a parte, se serve lavorare sul codice esistente.
