# Smart heating project
*Smart heating* to programowa część systemu centralnego ogrzewania realizująca założenia tzw. *inteligentnego domu*. Realizacja projektu umożliwia łatwe zarządzanie infrastrukturą ogrzewającą dom rodzinny. System składa się z poniższych komponentów, których oprogramowanie przedstawiono w poszczególnych folderach projektu o tej samej nazwie:
- ``server`` - centrum pobierające dane z czujników, przetwarzające je i przekazujące decyzje do aktuatorów. Jeden serwer obsługuje cały system. Realizuje:
  - ``receiver.py`` - program działający jako centrum przetwarzania informacji, tworzące bazę danych, odbierające komunikaty cały czas i wydające odpowiedzi, kiedy zachodzi taka potrzeba
  - ``gui.py`` program obsługujący interfejs graficzny, działający kiedy zachodzi taka potrzeba
- ``area`` - urządzenie skupiające funkcjonalności następujących podzespołów:
  - ``temperature_sensor`` - czujnik temperatury dokonujący okresowych pomiarów temperatury w pomieszczeniu. Jest on przypisany do danego *obszaru*. 
  - ``valve`` - zawór odcinający i otwierający dopływ ciepła do danego *obszaru* na podstawie wartości temperatury oczekiwanej i rzeczywistej.
- ``heating_unit`` - jednostka grzewcza, odbierająca od serwera informacje na temat potrzeby rozpoczęcia lub zakończenia ogrzewania.

Komunikacja między komponentami jest realizowana za pomocą protokołu MQTT bez uwierzytelniania.