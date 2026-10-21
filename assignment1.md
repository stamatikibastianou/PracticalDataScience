| Dataset | Task | Link to guidelines | Score (1-4) | Why this score | Author, reader or not stated | Quote |
|---|---|---|---|---|---|---|
| German ABSA 2026 | Sentiment | https://arxiv.org/abs/2605.03624 | 4 | Έχουν ορισμούς, παραδείγματα και κανόνες για δύσκολες περιπτώσεις (implicit aspects, conflict). | Author | "beschreibt den Grad der Positivität... die in der Meinung... ausgedrückt wird." |
| GoEmotions | Sentiment | https://arxiv.org/pdf/2005.00547 | 3 | Δίνουν ορισμούς και παραδείγματα, αλλά δεν έχουν αναλυτικούς κανόνες για σύνθετες περιπτώσεις. | Not stated | "Definitions for all emotions (short sentences and examples) are shown to annotators, standardizing interpretation." |
| Jigsaw Toxic Comment | Toxicity | https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge | 2 | Δίνει έναν βασικό ορισμό της τοξικότητας, αλλά λείπουν παραδείγματα και κανόνες για εξαιρέσεις. | Reader | "a rude, disrespectful, or unreasonable comment that is likely to make you leave a discussion" |
| Measuring Hate Speech | Toxicity | https://aclanthology.org/2022.nlperspectives-1.11/ | 4 | Παρέχει αναλυτική κλίμακα, ερωτηματολόγιο και ξεκάθαρους κανόνες για το τι (δεν) πρέπει να συμπεραίνουν οι annotators. | Reader | "Do not infer unavailable context, speaker identity, or intent." |

Step 3: Explanations
1. Weakest guidelines:
Το Jigsaw Toxic Comment Classification Challenge έλαβε τη χαμηλότερη βαθμολογία (2). Ενώ δίνει έναν βασικό ορισμό της τοξικότητας, απουσιάζουν εντελώς τα παραδείγματα κειμένων και οι ειδικοί κανόνες για το πώς πρέπει να χειρίζονται οι σημειωτές τις δύσκολες περιπτώσεις (π.χ. σαρκασμός ή εξαιρέσεις).

2. Whose feeling?:
Στη σκηνή του θανάτου του πολεμιστή, η διαφωνία θα προέκυπτε αν ο πρώτος σημειωτής ταυτιζόταν με την οργή του χαρακτήρα, ο δεύτερος αξιολογούσε την ψυχρή/αντικειμενική περιγραφή του αφηγητή και ο τρίτος έκρινε με βάση τη δική του θλίψη ως αναγνώστης. Το εγχειρίδιο του German ABSA 2026 θα το απέτρεπε αυτό, καθώς ζητά ρητά να κριθεί το συναίσθημα που "εκφράζεται στη γνώμη", εστιάζοντας άρα στον αφηγητή και όχι στην αντίδραση του αναγνώστη.

3. Write the fix:
"Αξιολογήστε αποκλειστικά το συναίσθημα που προκαλείται σε εσάς ως αναγνώστη του στίχου. Πρέπει να αγνοήσετε εντελώς τα συναισθήματα των χαρακτήρων που περιγράφονται ή το αντικειμενικό ύφος του αφηγητή."