# Smart heating project
*Smart heating* to propozycja realizacji programowej części systemu centralnego ogrzewania w koncepcji tzw. *inteligentnego domu*. Nasze rozwiązanie umożliwia łatwe zarządzanie infrastrukturą ogrzewającą dom rodzinny. Pomimo *centralności* systemu realizowany jest rozproszony model, w którym na decyzję o włączeniu jednostki grzewczej wpływają zadane przez użytkownika temperatury docelowe w i odczytane z czujników temperatury rzeczywiste w poszczególnych pomieszczeniach. System składa się z poniższych komponentów:
- ``server`` - centrum decyzyjne systemu. W skład jego oprogramowania wchodzą:
  - ``receiver.py`` - program przetwarzający dane z czujników i interfejsu graficznego w decyzje dotyczące ogrzewania. Tworzy bazę danych i zajmuje się jej zarządzaniem. Działa cały czas, nasłuchując komunikatów.
  - ``gui.py`` - program obsługujący interfejs graficzny, umożliwia odczyt aktualnego stanu układu i zmianę przez użytkownika docelowych temperatur w poszczególnych pomieszczeniach. Jego cykl życia nie wpływa na cykl życia systemu.
  - ``database_interface.py`` - zbiór rozwiązań pozwalających powyższym programom na sprawną komunikację z bazą danych na wyższym poziomie abstrakcji.
  - ``create_database.py`` - skrypt tworzący bazę danych i inicjalizujący jej początkowy stan.
  - ``decode.py`` - zbiór rozwiązań umożliwiających odczyt komunikacji w abstrakcji od jej struktury.
- ``area`` - abstrakcja reprezentująca jedno pomieszczenie, skupiająca w sobie *czujnik temperatury* i *zawór*, obsługiwane w projekcie następującymi skryptami:
  - ``area.py`` - program realizujący funkcjonalności i komunikację z serwerem dla urządzeń w pomieszczeniu.
  - ``temperature_sensor.py`` - skrypt obsługujący czujnik temperatury, który dokonuje okresowych pomiarów temperatury w pomieszczeniu.
  - ``valve.py`` - skrypt obsługujący zawór, który odcina i otwiera dopływ ciepła do danego *obszaru*. Jego obecność pozwala na ograniczenie dopływu ciepła z jednostki grzewczej do pomieszczeń, które są już ogrzane, a co za tym idzie bardziej efektywne zarządzanie energią. Decyzja o otwarciu i odcięciu dopływu ciepła jest podejmowana na podstawie zestawienia wartości temperatury docelowej z serwera z odczytem wartości temperatury rzeczywistej z czujnika, co realizuje paradygmat *edge computing* . 
  - ``display.py`` - skrypt realizujący podgląd stanu czujnika i zaworu w pomieszczeniu na urządzeniu *raspberry-pi*.
- ``heating_unit`` - jednostka grzewcza, odbierająca od serwera informacje na temat potrzeby rozpoczęcia lub zakończenia ogrzewania.
  - ``heat.py`` - skrypt odbierający i przetwarzający komunikację od serwera.
  - ``display.py`` - skrypt umożliwiający podgląd stanu jednostki na urządzeniu *raspberry-pi*.
  
Ponad to w projekcie znajdują się skrypty konfiguracyjne i skrypty grupujące funkcje umożliwiające powyższe funkcjonalności.

## Cykl życia programów

| Początek | Komponent       | Koniec   |
|:---------|:----------------|:---------|
| 1.       | ``receiver.py`` | -        |
| 1.       | ``heat.py``     | -        |
| Po 1.    | ``area.py``     | Dowolny* |
| Po 1.    | ``gui.py``      | Dowolny  |

*- przerwanie działania urządzenia danej strefy uniemożliwia jej wpływ na działanie jednostki grzewczej.

## Przepływ komunikatów

Komunikacja między komponentami jest realizowana za pomocą protokołu MQTT bez uwierzytelniania.

| Temat           | Nadawca                    | Odbiorca        | Opis                                                                                                                  |
|:----------------|:---------------------------|:----------------|:----------------------------------------------------------------------------------------------------------------------|
| ``ASK(id)``     | ``area.py(id)``/``gui.py`` | ``receiver.py`` | Zapytanie o dostarczenie do pomieszczenia informacji z bazy danych o oczekiwanej wartości temperatury w pomieszczeniu |
| ``DESIRED(id)`` | ``receiver.py``            | ``area.py(id)`` | Informacja o oczekiwanej wartości temperatury w pomieszczeniu, zapytanie o aktualną jej wartość                       |
| ``ACTUAL(id)``  | ``area.py(id)``            | ``receiver.py`` | Informacja o aktualnej wartości temperatury w pomieszczeniu                                                           |
| ``UPDATE(id)``  | ``receiver.py``            | ``gui.py``      | Informacja o potrzebie pobrania zaktualizowanej wartości temperatury z bazy danych                                    |
| ``HEATING``     | ``receiver.py``            | ``heat.py``     | Żądanie włączenia lub wyłączenia jednostki grzewczej                                                                  |


Projekt został zrealizowany w ramach laboratorium Podstaw Internetu Rzeczy.