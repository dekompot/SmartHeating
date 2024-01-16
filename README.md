# Smart heating project
*Smart heating* to programowa część systemu centralnego ogrzewania realizująca założenia tzw. *inteligentnego domu*. Realizacja projektu umożliwia łatwe zarządzanie infrastrukturą ogrzewającą dom rodzinny. System składa się z poniższych komponentów, których oprogramowanie przedstawiono w poszczególnych folderach projektu o tej samej nazwie:
- ``server`` - centrum pobierające dane z czujników, przetwarzające je i przekazujące decyzje do aktuatorów. Jeden serwer obsługuje cały system. Realizuje:
  - program odbierający komunikaty, działa cały czas
  - programy wydające komunikaty, kiedy zachodzi taka potrzeba
  - program obsługujący interfejs graficzny, kiedy zachodzi taka potrzeba
- ``temperature_sensor`` - czujnik temperatury dokonujący okresowych pomiarów temperatury w pomieszczeniu. Jest on przypisany do danego *obszaru*. W jednym obszarze może być wiele czujników. Działa okresowo, aby przesłać odczyt temperatury.
- ``valve`` - zawór odcinający i otwierający dopływ ciepła do danego *obszaru* na podstawie decyzji serwera. Cały czas działa i nasłuchuje tych decyzji.
- ``heating_unit`` - jednostka grzewcza, odbierająca od serwera informacje na temat potrzeby dostarczenia dodatkowego ciepła do instalacji. Zakładamy, że korzysta z niezależnego oprogramowania jej producenta w celu przetworzenia naszych żądań.

Ponadto, serwer obsługuje połączenie z  bazę danych ``temperatures.db``, do której zapisuje wszystkie odczyty i decyzje. Komunikacja na poziomie internetu rzeczy między komponentami jest realizowana za pomocą protokołu MQTT.