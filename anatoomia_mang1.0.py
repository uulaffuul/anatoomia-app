import os
import random
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import re

# ASUKOHT
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "pildid")

# --- TÄIELIK ANDMEBAAS ---
INFO_DB = {
    "suboccipitalis": {"n": "kuklaalune lihas", "a": "C1, C2", "k": "C1, Occiput (kuklaluu)", "f": "Kaela / pea stabiliseerimine"},
    "erectorspinae": {"n": "lülisamba sirgestajad", "a": "Occiput (kuklaluu)", "k": "Sacrum (ristluu)", "f": "Selja stabiliseerimine"},
    "supraspinatus": {"n": "harjaüline lihas", "a": "Scapula (abaluu)", "k": "Tuberculum majus", "f": "GH liigese välimine rotatsioon ja abduktsioon"},
    "infraspinatus": {"n": "harjaalune lihas", "a": "Scapula (abaluu)", "k": "Tuberculum majus", "f": "Välimine rotatsioon + GH liigese stabilisatsioon"},
    "teresminor": {"n": "väike ümarlihas", "a": "Scapula (abaluu)", "k": "Tuberculum majus", "f": "Välimine rotatsioon + GH liigese stabilisatsioon"},
    "subscapularis": {"n": "abaluualune lihas", "a": "Scapula (anterior)", "k": "Tuberculum minus", "f": "Sisemine rotatsioon + GH liigese stabilisatsioon"},
    "deltoideus": {"n": "deltalihas", "a": "Clavicula, acromion, spina scapula", "k": "Humerus", "f": "Õlaliigese abduktsioon, ekstensioon, fleksioon"},
    "trapezius": {"n": "trapetslihas", "a": "Occiput, C7", "k": "Clavicula, acromion, spina scapula", "f": "Abaluu tõstmine ja stabiliseerimine"},
    "serratusanterior": {"n": "eesmine saaglihas", "a": "Scapula (margo medialis)", "k": "Costa 1-9 (roided)", "f": "Protraktsioon, stabiliseerib abaluud"},
    "rhomboideii": {"n": "romblihased", "a": "Spinaalsed jätked (C7-T5)", "k": "Margo medialis scapula", "f": "Abaluu retraktsioon"},
    "latissimusdorsi": {"n": "selja lailihas", "a": "Spinaalsed jätked (T7-L5)", "k": "Tuberculum minus", "f": "Õla adduktsioon, ekstensioon ja siserotatsioon"},
    "tricepsbrachii": {"n": "õlavarre kolmpealihas", "a": "Scapula, humerus", "k": "Olecranon", "f": "Küünarliigese ekstensioon"},
    "bicepsbrachii": {"n": "õlavarre kakspealihas", "a": "Scapula (proc. coracoideus)", "k": "Radius (radial tuberosity)", "f": "Küünarliigese fleksioon ja supinatsioon"},
    "brachialis": {"n": "õlavarrelihas", "a": "Humerus (anteriort)", "k": "Ulna (proximalt)", "f": "Küünarliigese fleksioon"},
    "coracobrachialis": {"n": "kaarnajätke-õlavarrelihas", "a": "Proc. coracoideus", "k": "Humerus", "f": "Õlaliigese fleksioon"},
    "brachioradialis": {"n": "õlavarre-kodarluulihas", "a": "Humerus (distalt)", "k": "Radius (distalt)", "f": "Küünarliigese fleksioon"},
    "kasivarrepainutajalihased": {"n": "randme painutajad", "a": "Humerus", "k": "Carpalben, phalanger", "f": "Küünarliigese, randmete ja sõrmede fleksioon"},
    "kasivarresirutajalihased": {"n": "randme sirutajad", "a": "Humerus", "k": "Carpalben, phalanger", "f": "Randme ja sõrmede ekstensioon"},
    "pectoralismajor": {"n": "suur rinnalihas", "a": "Sternum, clavicula, costa 2-7", "k": "Humerus", "f": "Õla horisontaalne adduktsioon"},
    "pectoralisminor": {"n": "väike rinnalihas", "a": "Proc. coracoideus", "k": "Costa 3-5 (roided)", "f": "Langetab abaluud, kergitab roidepaari"},
    "rectusabdominis": {"n": "kõhu sirglihas", "a": "Costa 5-7", "k": "Pubis (häbemeluu)", "f": "Kere fleksioon, kompressioon"},
    "obliquusexternus": {"n": "välimine kõhu põikilihas", "a": "Costa 5-12", "k": "Iliac crest, linea alba", "f": "Kere fleksioon ja rotatsioon"},
    "obliquusinternus": {"n": "sisemine kõhu põikilihas", "a": "Fascia thoracolumbalis", "k": "Roided 10-12", "f": "Kere fleksioon ja rotatsioon"},
    "transversusabdominis": {"n": "kõhu ristilihas", "a": "Fascia thoracolumbalis", "k": "Linea alba", "f": "Lülisamba stabiliseerimine"},
    "diaphragma": {"n": "vahelihas", "a": "Roided 7-12, nimmelülid L1-L3", "k": "Centrum tendineum", "f": "Hingamislihas, tekitab kõhusurvet"},
    "psoasmajor": {"n": "suur nimmelihas", "a": "L1-L5", "k": "Trochanter minor", "f": "Puusaliigese fleksioon"},
    "iliacus": {"n": "niudelihas", "a": "Ilium (anterior)", "k": "Trochanter minor", "f": "Puusaliigese fleksioon"},
    "gluteusmedius": {"n": "keskmine tuharalihas", "a": "Ilium (lateral)", "k": "Trochanter major", "f": "Puusa abduktsioon"},
    "gluteusmaximus": {"n": "suur tuharalihas", "a": "Ilium, sacrum", "k": "Femur (posterior)", "f": "Puusa ekstensioon"},
    "piriformis": {"n": "pirnlihas", "a": "Sacrum", "k": "Trochanter major", "f": "Välimine rotatsioon"},
    "tensorfascialatae": {"n": "lai-sidekirme pingutaja", "a": "Ilium", "k": "Tibia (lateral)", "f": "Puusa fleksioon ja abduktsioon"},
    "adductorlongusbrevis": {"n": "pikk/lühike lähendaja", "a": "Pubis", "k": "Femur (posterior)", "f": "Puusa adduktsioon ja fleksioon"},
    "adductormagnus": {"n": "suur lähendajalihas", "a": "Pubis, Ischium", "k": "Femur (posterior)", "f": "Puusa adduktsioon ja ekstensioon"},
    "quadricepsfemoris": {"n": "reie nelipealihas", "a": "Ilium, femur", "k": "Patella, Tuberositas tibia", "f": "Põlveliigese ekstensioon"},
    "sartorius": {"n": "rätseplihas", "a": "Ilium (SIAS)", "k": "Tibia (medial)", "f": "Puusaliigese fleksioon, adduktsioon, rotatsioon, põlve fleksioon"},
    "hamstring": {"n": "reie tagakülje lihased", "a": "Pelvis, Ischium", "k": "Tibia, Fibula", "f": "Põlve fleksioon, puusa ekstensioon"},
    "gracilis": {"n": "õrnlihas", "a": "Pubis", "k": "Tibia (medial)", "f": "Puusa adduktsioon"},
    "peroneuslongusbrevis": {"n": "pikk/lühike pindluulihas", "a": "Fibula", "k": "1st metatarsal, medial cuneiform", "f": "Plantaarfleksioon"},
    "tibialisanterior": {"n": "eesmine sääreluulihas", "a": "Tibia (anteriort)", "k": "1st metatarsal", "f": "Dorsaalfleksioon"},
    "gastrocnemius": {"n": "sääre kakspealihas", "a": "Femur (distalt)", "k": "Calcaneus", "f": "Plantaarfleksioon, põlve fleksioon"},
    "soleus": {"n": "lestlihas", "a": "Tibia + fibula", "k": "Calcaneus", "f": "Plantaarfleksioon"},
    "tibialisposterior": {"n": "tagumine sääreluulihas", "a": "Tibia + Fibula", "k": "Navicular, medial cuneiform", "f": "Plantaarfleksioon, inversioon"}
}

class AnatomyMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("Anatoomia Master (Horisontaalne)")
        self.root.geometry("1300x750")
        self.root.configure(bg="#2c3e50")
        self.skoor = 0
        self.etapp = "nimi"

        if not os.path.exists(IMAGE_FOLDER):
            messagebox.showerror("Viga", "Piltide kausta ei leitud!")
            root.destroy()
            return

        self.all_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        self.loo_liides()
        self.uue_kordus()

    def loo_liides(self):
        # Ülemine riba
        self.top_frame = tk.Frame(self.root, bg="#34495e", height=50)
        self.top_frame.pack(fill="x")
        
        # ANDMEBAASI NUPP
        tk.Button(self.top_frame, text="AVA ANDMEBAAS", command=self.ava_andmed, bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=20, pady=5)
        
        self.info_label = tk.Label(self.top_frame, text="Skoor: 0", font=("Arial", 14), fg="white", bg="#34495e")
        self.info_label.pack(side="right", padx=20)

        # Peamine raam
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.left_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.img_label = tk.Label(self.left_frame, bg="#2c3e50")
        self.img_label.pack(pady=20)

        self.right_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.right_frame.pack(side="right", fill="both", padx=20)

        self.ques_label = tk.Label(self.right_frame, text="", font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#2c3e50", wraplength=500, justify="left")
        self.ques_label.pack(pady=(20, 10))

        self.btn_frame = tk.Frame(self.right_frame, bg="#2c3e50")
        self.btn_frame.pack()
        self.buttons = []
        for i in range(3):
            btn = tk.Button(self.btn_frame, text="", font=("Arial", 10), width=60, height=2, command=lambda idx=i: self.kontrolli(idx))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.feedback_label = tk.Label(self.right_frame, text="", font=("Arial", 12, "bold"), bg="#2c3e50", pady=10)
        self.feedback_label.pack()
        self.next_btn = tk.Button(self.right_frame, text="JÄRGMINE LIHAS >>", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", command=self.uue_kordus, padx=20, pady=10)

    def ava_andmed(self):
        aken = tk.Toplevel(self.root)
        aken.title("Lihaste andmebaas")
        aken.geometry("1000x600")
        cols = ("Ladina", "Eesti", "Algus", "Kinnitus", "Funktsioon")
        tree = ttk.Treeview(aken, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        for voti in sorted(INFO_DB.keys()):
            d = INFO_DB[voti]
            tree.insert("", "end", values=(voti, d['n'], d['a'], d['k'], d['f']))
        tree.pack(fill="both", expand=True)

    def puhasta(self, nimi):
        t = nimi.lower()
        t = re.sub(r'\.(jpg|jpeg|png|webp)$', '', t)
        t = re.sub(r'^\d+[\s\.\-_]*', '', t)
        t = t.replace("mm.", "").replace("m.", "").replace("mm ", "").replace("m ", "")
        return "".join(c for c in t if c.isalpha())

    def uue_kordus(self):
        self.next_btn.pack_forget()
        self.feedback_label.config(text="")
        self.etapp = "nimi"
        self.oige_fail = random.choice(self.all_files)
        self.oige_voti = self.puhasta(self.oige_fail)
        img = Image.open(os.path.join(IMAGE_FOLDER, self.oige_fail))
        img.thumbnail((700, 500))
        self.tk_pilt = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.tk_pilt)
        self.uuenda_etappi()

    def uuenda_etappi(self):
        andmed = INFO_DB.get(self.oige_voti, {"n": "Tundmatu", "a": "?", "k": "?", "f": "?"})
        if self.etapp == "nimi":
            self.ques_label.config(text="1. Mis lihas see on?")
            valikud = [self.oige_fail]
            while len(valikud) < 3:
                lisa = random.choice(self.all_files)
                if self.puhasta(lisa) != self.oige_voti and lisa not in valikud: valikud.append(lisa)
            random.shuffle(valikud)
            self.praegused_valikud = valikud
            for i in range(3): self.buttons[i].config(text=os.path.splitext(valikud[i])[0], bg="white", state="normal")
        elif self.etapp == "algus":
            self.ques_label.config(text=f"Õige! See on {andmed['n']}.\n2. Vali ALGUSKOHT (A):")
            self.loo_andmete_valikud('a')
        elif self.etapp == "kinnitus":
            self.ques_label.config(text=f"Algus: {andmed['a']}\n3. Vali KINNITUSKOHT (K):")
            self.loo_andmete_valikud('k')
        elif self.etapp == "funktsioon":
            self.ques_label.config(text=f"Kinnitus: {andmed['k']}\n4. Vali FUNKTSIOON (F):")
            self.loo_andmete_valikud('f')

    def loo_andmete_valikud(self, liik):
        oige_vastus = INFO_DB[self.oige_voti][liik]
        koik_vastused = list(set([v[liik] for v in INFO_DB.values() if v[liik] != oige_vastus]))
        valikud = random.sample(koik_vastused, 2) + [oige_vastus]
        random.shuffle(valikud)
        self.praegused_valikud = valikud
        for i in range(3): self.buttons[i].config(text=valikud[i], bg="white", state="normal")

    def kontrolli(self, idx):
        valik = self.praegused_valikud[idx]
        andmed = INFO_DB[self.oige_voti]
        if self.etapp == "nimi": vastus_on_oige = (self.puhasta(valik) == self.oige_voti)
        else:
            liik = self.etapp[0] if self.etapp != "funktsioon" else "f"
            vastus_on_oige = (valik == andmed[liik])
        if vastus_on_oige:
            self.feedback_label.config(text="ÕIGE!", fg="#2ecc71")
            if self.etapp == "nimi": self.etapp = "algus"
            elif self.etapp == "algus": self.etapp = "kinnitus"
            elif self.etapp == "kinnitus": self.etapp = "funktsioon"
            elif self.etapp == "funktsioon":
                self.skoor += 1
                self.info_label.config(text=f"Skoor: {self.skoor}")
                self.etapp = "lopp"
                self.feedback_label.config(text="KÕIK VASTUSED ÕIGED!", fg="#f1c40f")
                for b in self.buttons: b.config(state="disabled")
                self.next_btn.pack(pady=20)
                return
            self.root.after(400, self.uuenda_etappi)
        else:
            self.feedback_label.config(text="VALE!", fg="#e74c3c")
            self.buttons[idx].config(bg="#fab1a0", state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnatomyMaster(root)
    root.mainloop()
