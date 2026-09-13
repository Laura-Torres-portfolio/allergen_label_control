# 🛡️ SafeLabel & Allergen Shield: Digital Quality & Food Safety Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Sistema digital end-to-end para el control de alérgenos alimentarios, liberación pre-operativa basada en bioluminiscencia ATP (3M Clean-Trace) y auditoría de etiquetado en tiempo real mediante Visión Artificial (OCR).**

---

## 📌 Contexto y Problema de Negocio

En la industria agroalimentaria y de gran consumo (FMCG), las contaminaciones cruzadas por alérgenos y los errores en el etiquetado representan la **causa #1 de retiradas de producto (*recalls*)** en la UE y FDA. Estas incidencias generan pérdidas económicas millonarias, paradas no programadas de planta y graves riesgos para la salud pública.

### Desafíos Operativos Clave:
1. **Ineficiencia en Limpiezas Intermedias:** Limpiar a fondo entre cada lote reduce drásticamente la efectividad global del equipo (*OEE*). Las fábricas programan la producción de menor a mayor carga de alérgenos, pero la falta de trazabilidad digital en el arrastre (*carry-over*) provoca fallos de inocuidad.
2. **Subjetividad en Liberaciones Pre-operativas:** Falta de integración en tiempo real de los datos de luminometría nocturna (ATP en RLU) con la planificación diaria de envasado.
3. **Error Humano en Envasado:** Desajustes entre la receta programada y la etiqueta física impresa al final de la línea.

---

## 💡 Solución Digital Propuesta

**SafeLabel & Allergen Shield** unifica la telemetría higiénica nocturna, los algoritmos de secuenciación de producción y la visión artificial en un único **Dashboard Operativo en Streamlit** para el departamento de Calidad y Seguridad Alimentaria.

```text
                                ARQUITECTURA DEL SISTEMA
                                
 ┌──────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
 │ 1. Limpieza Nocturna │ ──>│ 2. Matriz Secuenciación  │ ──>│ 3. Inspección OCR Label  │
 │  3M Clean-Trace ATP  │    │  Arrastre de Alérgenos   │    │ Visión Artificial Línea  │
 └──────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
            │                             │                               │
            └─────────────────────────────┼───────────────────────────────┘
                                          ▼
                         ┌─────────────────────────────────┐
                         │  Dashboard Streamlit / Power BI │
                         │  Liberación / Hold de Lotes     │
                         └─────────────────────────────────┘
```
## 🚀 Guía de Instalación y Ejecución de la App

Sigue estos pasos para ejecutar la aplicación **SafeLabel & Allergen Shield** en tu ordenador local.

---

### 📋 Prerrequisitos

Asegúrate de tener instalado en tu sistema:
* **Python 3.9 o superior** (comprueba tu versión corriendo `python --version` o `python3 --version` en la consola).
* **Git** (opcional, para clonar el repositorio).

---

### 💻  Ejecuta la App desde el siguiente enlace:
* **Demo App:** [allergen-label-control.streamlit.app](https://allergen-label-control.streamlit.app)
  
## 👤 Autora
* **Perfil:** Laura Torres | Especialista en Digital Quality, Food Safety & Big Data.
* **GitHub:** [Laura-Torres-portfolio](https://github.com/Laura-Torres-portfolio)
