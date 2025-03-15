class Location:
    def __init__(self, address: str, coordinates: dict):
        self._address = address
        self._coordinates = [coordinates["lat"], coordinates["lng"]]  # In lat/long format
        self._temperature = 0.0
        self._precipitation = 0.0
        self._currentTime = ""
        self._population = 0

    # Getters
    def getAddress(self) -> str:
        return self._address

    def getCoordinates(self) -> list:
        return self._coordinates

    def getTemperature(self) -> float:
        return self._temperature

    def getPrecipitation(self) -> float:
        return self._precipitation

    def getCurrentTime(self) -> str:
        return self._currentTime
    
    def getPopulation(self) -> int:
        return self._currentTime

    # Setters
    def setAddress(self, address: str):
        self._address = address

    def setCoordinates(self, lat: float, lng: float):
        self._coordinates = [lat, lng]

    def setTemperature(self, temperature: float):
        self._temperature = temperature

    def setPrecipitation(self, precipitation: float):
        self._precipitation = precipitation

    def setCurrentTime(self, current_time: str):
        self._currentTime = current_time

    def setPrecipitation(self, current_time: str):
        self._currentTime = current_time

    def __str__(self):
        return (f"Address: {self._address}\n"
                f"Coordinates: {self._coordinates}\n"
                f"Temperature: {self._temperature}\n"
                f"Precipitation: {self._precipitation}\n"
                f"Current Time: {self._currentTime}")
