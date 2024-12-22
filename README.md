[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/jsTzsySB)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=15155144)
# Proposal: Aplikacja do rezerwacji lotów
![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/b647d3e1-2b31-447e-abcb-392efe809e3d)

---
## (Dokumentacja poniżej)
---

### Skład grupy: Hanna Nużka, Tobiasz Salik, Jakub Teichman, Martyna Trytko

Cel projektu: stworzenie aplikacji webowej, która umożliwia rezerwację miejsc w samolocie. Aplikacja ma za zadanie ułatwić proces wyszukiwania lotów, wyboru miejsc oraz dokonywania rezerwacji, a także dostarczyć użytkownikom wszystkie niezbędne informacje dotyczące podróży, takie jak informacje o bagażu, podróżowaniu ze zwierzętami, dostępnych posiłkach i napojach oraz udostępnić dane kontaktowe.

### Wykorzystane technologie:
•	Python
•	Flask
•	HTML
•	Bootstrap
•	jQuery
•	SQLite
•	UUID
•	Web Scraping (BeautifulSoup)

### Opis aplikacji:
Aplikacja oferuje następujące funkcjonalności:
1.	Strona główna umożliwiająca użytkownikom wyszukiwanie lotów poprzez podanie miejsca wylotu, miejsca docelowego, daty podróży
2.	Wyniki wyszukiwania lotów wyświetlają dostępne loty spełniające kryteria wyszukiwania
3.	Wybór miejsca umożliwia użytkownikom wybór miejsca w samolocie
4.	Formularz rezerwacyjny umożliwia użytkownikom wprowadzenie danych osobowych i dokonanie rezerwacji wybranego miejsca
5.	 Potwierdzenie rezerwacji wyświetla szczegóły rezerwacji

Dodatkowo aplikacja zawiera następujące podstrony informacyjne:
•	nasza flota- informacje o samolotach
•	bagaż- informacje odnośnie dozwolonego limitu, dodatkowych kosztach
•	podróżowanie ze zwierzętami- zasady podróży ze zwierzętami, koszty
•	posiłki i napoje

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/a36c1d7e-3fb0-4a5f-bd74-56465b23400c)






---
# Dokumentacja projektu:
---
Nasz projekt ma na celu umożliwienie wyszukania użytownikowi połączenia lotniczego z wybranego miasta do miasta docelowego oraz rezerwacje danego miejsca w samolocie. Aplikacja ułatwia proces wyszukiwania dzięki prostej w obsłudze aplikacji webowej jak i intuicyjnej wyszukiwarce lotów, dodatkowo dzięki innym podstronom widocznym na pasku wyszukiwania- na górze aplikacji użytkownik może przeczytać o praktycznych informacjach dotyczących bagażu, podróży ze zwierzętami, posiłkach i napojach. Po zalogowaniu się użytkownik może zobaczyć zarezerwowane przez siebie loty, a osoba z rolą administratora może zobaczyć wszystkie zarezerwowane przez użytkowników loty i edytować je w razie takiej konieczności.

### Do tworzenia strony wykorzystaliśmy następujące technologie:
- HTML
- Flask
- Bootstrap
- Python
- SQLite
- UUID
- Web Scraping (BeautifulSoup)

### Opis aplikacji:
Po wejściu na stronę główną każdy użytkownik może dokonać wyszukiwania połączeń lotniczych, poczytać o wybranych miastach do których można się udać na wycieczkę, zobaczyć partnerów firmy, a także zobaczyć politykę firmy oraz social media, do których odnośniki znajdują się w stopce aplikacji. Użytkownik, dzięki paskowi nawigacji dostępnym na górze strony, może również przeczytać o flocie samolotowej, bagażu i informacjach na temat wymiarów, wagi czy rzeczy, które się mogą w nim znajdować, podróży ze zwierzętami- wymaganych dokumentach, dozwolonych typach zwierzaków, które można przewzić, posiłkach i napojach a także możliwości kontaktu z firmą. 
Aby dokonać rezerwacji trzeba posiadać konto na naszej aplikacji, aby się zarejestrować wystarczy nakliknąc przycik znajdujący się na górze ekranu i wypełnić krótki formularz rejestracji, a następnie się zalogować to pozwala nam na dokonanie rezerwacji poprzez wypełnienie formularza z danymi osobowymi oraz wybór miejsca ze stworzonego widoku pokładu samolotu, dodatkowo możemy już przy rejestracji wybrać z jakim bagażem chcemy podróżować i czy decydujemy się na ubezpieczenie. Aby uniknąć sytuacji, w której więcej niż jedna osoba wybiera to samo miejsce wprowadziliśmy ograniczenie czasowe 15 minut podczas wyboru miejsca. 
Dodatkowo na panelu zalogowanego użytkownika jest możliwość podglądu swoich rezerwacji, a na panelu administratora jest możliwość zobaczenia wszystkich dokonanych rezerwacji oraz w razie konieczności takiej jak zła pogoda, odwołać lot lub go zmodyfikować, np. dodając opóźnienie. 

## Działanie aplikacji:
# 1. Wyszukiwanie lotów: 
Użytkownik może dokonać rezerwacji lotu poprzez wypełnienie formularza. W pola, gdzie należy wpisać miejsce wylotu oraz przylotu można wpisać zarówno nazwę miasta, jak i kod IATA lotniska, które bezpośrednio wskazuje na konkretne lotnisko.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/bbf2c6fa-3aad-4619-aa83-59555115aac4)

Jeżeli wskazane miasto posiada więcej niż jedno lotnisko, to jest wyświetlana lista lotnisk z kodami IATA dla danego miasta: np. dla miasta Madryt: Barajas, MAD; Torrejon Afb, TOJ
Wówczas użytkownik powinien zdecydować na które lotnisko chce się dostać i w formularzu wskazać konkretne lotnisko.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/879fa55c-727b-4574-9229-26cc1899a0b4)

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/68647ffc-fdfb-438b-809b-f76a0749790b)

Wyszukiwanie lotów odbywa się w oparciu o Web Scraping ze strony https://www.flightconnections.com/, która gromadzi i udostępnia dane na temat połączeń lotniczych. Gdy użytkownik wprowadza miejsce wylotu i przylotu, to miasta są zamieniane na kody IATA lotnisk i następnie wprawdzane jest czy połączenie (bezpośrednie) wskazane przez użytkownika istnieje oraz jacy przewoźnicy oferują taki przelot. 
![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/a9f0bf28-eae3-407c-ab82-514f4a4b51bd)

# 2. Tworzenie rezerwacji
Rezerwacje może dokonać tylko zarejestrowany użytkownik. Jeżeli wyszukanie lotu przebiegło pomyślnie (wybrane połączenie lotnicze istnieje) to wyświetlane są linie lotnicze, które oferują takie połączenie i użytkownik powinien wskazać, którego przewoźnika wybiera.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/3f4d5795-c0d7-4cfd-8e77-b2a26f092cbd)

W kolejnym kroku należy wypełnić formularz z danymi osobowymi osoby rezerwującej lot.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/9cf35a36-234e-4059-9394-04bdc798f242)

Następnie należy wybrać miejsce w samolocie. Zielone oznaczenie to miejsce wolne. Szare wskazuje że jest zajęte.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/56020dd6-ef48-4894-8146-2d69aad9c7f7)

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/5cd5dbbd-c990-473a-b4c9-3da06f9627d1)

W tej części tworzenia rezerwacji widoczny jest odliczany czas na górze strony. Po jego upływie (15 minut) użytkownik zostaje przekierowany na stronę główną w celu ponownego dokonania rezerwacji. Takie rozwiązanie ma służyć ograniczeniu pozornego blokowania miejsc w samolocie dla innych użytkowników, który chcą dokonać rezerwacji na ten sam lot. 

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/18335334-84c8-4db4-a8ed-a8645dc15acc)


W ostatnim kroku należy wybrać opcje bagażu i ubezpieczenia.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/e4f5f181-19e6-4120-91e3-bbfe5b37bcdd)

Jeżeli w formularzu wyszukiwania lotu została zaznaczona opcja z biletem powrotnym (return ticket) to następnie zostaniemy przekierowani ponownie do opcji wyboru miejsca (tym razem biletu powrotnego), a kolejne kroki przebiegają analogicznie. Jeżeli bilet był w jedną stronę to odrazu zostaniemy przekierowani do widoku naszych rezerwacji.
![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/7860058f-3b13-4ac1-b9d1-ac203dbc5ae0)

Użytkownik może usunąć rezerwację albo ją edytować - podczas edycji możliwa jest tylko zmiana miejsca i zmiana opcji bagażu i ubezpieczenia.

Utworzona rezerwacja jest przypisywana do lotu (utworzonego, jeżeli dana rezerwacja na lot była pierwsza lub już istniejącego)

# 3. Funkcje admina

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/938f1a26-3f06-46ce-82ce-9a553fe4b2e1)

Admin (domyśle dane logowania: login i hasło: admin) posiada możliwość wglądu do utworzonych lotów i rezerwacji. 
Może przeglądać utworzonych użytkowników.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/6880de09-23b9-4d30-960a-6b2e6609471f)

A także mieć widok na wszystkie loty na które zostały złożone rezerwacje.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/2b5a5b7e-7960-4bd1-b0b9-6bd2a5a639f9)

Klikając opcje "More" można zobaczyć podstawowe dane na temat lotu oraz informacje o rezerwacjach na ten konkretny lot (imie, nazwisko, miejsce, bagaż itd.)

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/3f966e47-da14-4aa2-b0e3-05ac48ffafc7)

Klikając w ikone kosza można usunąć lot, np. w przypadku gdy konieczne jest odwołanie przelotu przez np. warunki pogodowe czy zdarzenia losowe.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/63361acd-31e1-414a-ab3d-6d89cbc31e29)

W przypadku usunęcia lotu, usuwane są wszystkie rezerwacje przypisane do lotu. Dla przykładu usunięty został lot LO8. Użytkownik, który na powyższych zdjęciach miał taką rezerwację - już jej nie ma.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/bd4a855a-79af-443e-9316-17941731e8f4)

Lot można także edytować wybierając na panelu admina opcje 'Edit'. Wtedy możliwa jest edycja lub usunięcie lotu przez wybranie odpowiedniej opcji w oknie przy wybranym locie. 

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/d94b5cff-5e51-47f6-ad01-cff0dcdf68cc)

Podczas edycji możliwe jest np. nadanie lotowi statusu lotu opóźnionego.

![image](https://github.com/grochot-agh/projekt-planetickets/assets/161709306/8381d5cb-6cb6-4a47-966c-2563e2abd667)


# Jak uruchomic projekt?

### Wymagania wstępne
Upewnij się, że masz zainstalowane następujące oprogramowanie:
- Python
- Git

### Sklonuj repozytorium
Najpierw sklonuj repozytorium na swój komputer za pomocą następującego polecenia:

```bash
git clone https://github.com/grochot-agh/projekt-planetickets.git
```


### Przejdź do katalogu projektu

Przejdź do katalogu, w którym zostało zklonowane repozytorium 

### Utwórz środowisko wirtualne

Zaleca się utworzenie środowiska wirtualnego w celu zarządzania zależnościami projektu. Użyj następujących poleceń:

```bash
python -m venv venv
```

Aktywuj środowisko wirtualne:

- Na systemie Windows:
  ```bash
  .\venv\Scripts\activate
  ```
- Na systemie macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### Zainstaluj zależności

Zainstaluj wszystkie niezbędne biblioteki z pliku `requirements.txt` za pomocą poniższego polecenia:

```bash
pip install -r requirements.txt
```

### Uruchom aplikację

Aby uruchomić aplikację, użyj następującego polecenia:

```bash
python app.py
```

Aplikacja będzie aktywna na porcie 5000. Możesz uzyskać do niej dostęp, otwierając przeglądarkę internetową i wchodząc na adres:

```
http://127.0.0.1:5000
```

### Dodatkowe informacje

W przypadku pytań lub problemów, prosimy o kontakt poprzez otwarcie zgłoszenia (issue) w repozytorium GitHub.

---

### Informacje dla testerów:
Jeżeli chcesz przetestować naszą aplikację, możesz w tym celu wykorzytać dane logowania dla dwóch rodzajów użytkowników:
- pax:
  - login: kuba
  - hasło: lato

- admin:
  - login: admin
  - hasło: admin

--- 

Dziękujemy za korzystanie z naszej aplikacji!














