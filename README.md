# Challenge Mutantes
![coverage](https://img.shields.io/badge/coverage-97%25-yellowgreen)

_Magneto quiere reclutar la mayor cantidad de mutantes para poder luchar contra los X-Men, esta aplicacion permite a traves del analisis del ADN enviado conocer si un humano es mutante o no._

  
  

## Comenzando

  

### Pre-requisitos 📋 

 - Python 3
 - pip

### Instalación 

  

_Instalar las librerias requeridas:_

  

```bash

pip install -r requirements.txt

```



### Ejecución

  

_Ejecutar con python el archivo principal main.py:_

  

```bash

python main.py

```

  

## Servicios disponibles

```
/mutant
/stats
```

### /mutant
El servicio “/mutant” en donde se pueda detectar si un humano es mutante enviando la secuencia de ADN mediante un HTTP POST con un Json el cual tenga el siguiente formato: 
 ```bash

POST → /mutant/ 
{ 
	“dna”:["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"] 
}

```

En caso de verificar un mutante, devuelve un HTTP 200-OK, en caso contrario un 403-Forbidden

### /stats
El servicio “/stats” devuelve un Json con las estadísticas de las verificaciones de ADN: 
   ```bash

{
	“count_mutant_dna”:40, “count_human_dna”:100: “ratio”:0.4
}

```

## Ejecutando las pruebas 

  

_Para ejecutar las pruebas automatizadas, ejecutar con python el archivo test.py:_

```bash

python test.py

```

  

### Resultados esperados de las pruebas

  

_Explica que verifican estas pruebas y por qué_

  

```

['ATGCGAA', 'CCGTGCC', 'TTATGTA', 'AGAAGGA', 'CACCTAT', 'TCACTGT', 'TTGTTGT']
.['ATGCGAA', 'CCGTGCC', 'TTATGTA', 'AGAAGGA', 'CACCTAT', 'TCACTGT', 'TTTTTGT']
.['ATGCGAA', 'CCGTGCC', 'TTATGTA', 'AGAAGGA', 'CACCTAT', 'TCACTGT', 'TTTTTGT']
...
----------------------------------------------------------------------
Ran 5 tests in 1.972s

OK

```
## Demo

```
http://ec2-54-175-201-155.compute-1.amazonaws.com/mutant
http://ec2-54-175-201-155.compute-1.amazonaws.com/stats
```

## Code Coverage

```
Name      Stmts   Miss  Cover
-----------------------------
main.py     100      3    97%
test.py      32      1    97%
-----------------------------
TOTAL       132      4    97%
```