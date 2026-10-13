"""Datos del Lab 05. No lo tocás.

- TMDL_MODELO: el modelo semántico de una hormigonera (el documento largo).
- RESULTADO_GET_MEDIDA: lo que devuelve la tool get_medida, con TODOS los campos que trae el TMDL.
- PREGUNTA: lo que pregunta el analista en este turno.
"""

PREGUNTA = (
    "¿Qué medida calcula [Ventas Netas], de qué columnas depende y por qué podría dar "
    "$1.250.430 en octubre cuando el ERP dice $1.310.000?"
)

TMDL_MODELO = """\
model Model
	culture: es-AR
	defaultPowerBIDataSourceVersion: powerBI_V3

table fVentas
	lineageTag: 4f1c2a10-77de-4c1b-9d0e-1a2b3c4d5e01

	column IdRemito
		dataType: int64
		summarizeBy: none
		sourceColumn: id_remito
		lineageTag: 4f1c2a10-77de-4c1b-9d0e-1a2b3c4d5e02

	column Fecha
		dataType: dateTime
		formatString: yyyy-mm-dd
		sourceColumn: fecha
		lineageTag: 4f1c2a10-77de-4c1b-9d0e-1a2b3c4d5e03

	column IdCliente
		dataType: int64
		summarizeBy: none
		sourceColumn: id_cliente
		lineageTag: 4f1c2a10-77de-4c1b-9d0e-1a2b3c4d5e04

	column IdProducto
		dataType: int64
		summarizeBy: none
		sourceColumn: id_producto
		lineageTag: 4f1c2a10-77de-4c1b-9d0e-1a2b3c4d5e05

	column M3
		dataType: decimal
		summarizeBy: sum
		sourceColumn: m3
		lineageTag: 4f1c2a10-77de-4c1b-9d0e-1a2b3c4d5e06

	column Monto
		dataType: decimal
		formatString: \\$#,0.00
		summarizeBy: sum
		sourceColumn: monto
		lineageTag: 4f1c2a10-77de-4c1b-9d0e-1a2b3c4d5e07

	column Estado
		dataType: string
		summarizeBy: none
		sourceColumn: estado
		lineageTag: 4f1c2a10-77de-4c1b-9d0e-1a2b3c4d5e08
		/// Valores: ENTREGADO, ANULADO, PENDIENTE_FACTURA

	partition fVentas-2026-10 = m
		mode: import
		source = Sql.Database("dwh", "ventas", [Query="SELECT * FROM remitos WHERE fecha >= '2026-10-01' AND fecha < '2026-10-31'"])

table dCliente
	lineageTag: 7a7b7c7d-1111-4aaa-8bbb-000000000001

	column IdCliente
		dataType: int64
		isKey
		sourceColumn: id_cliente
		lineageTag: 7a7b7c7d-1111-4aaa-8bbb-000000000002

	column Cliente
		dataType: string
		sourceColumn: razon_social
		lineageTag: 7a7b7c7d-1111-4aaa-8bbb-000000000003

	column Segmento
		dataType: string
		sourceColumn: segmento
		lineageTag: 7a7b7c7d-1111-4aaa-8bbb-000000000004

table dProducto
	lineageTag: 9e9e9e9e-2222-4ccc-9ddd-000000000001

	column IdProducto
		dataType: int64
		isKey
		sourceColumn: id_producto
		lineageTag: 9e9e9e9e-2222-4ccc-9ddd-000000000002

	column TipoHormigon
		dataType: string
		sourceColumn: tipo
		lineageTag: 9e9e9e9e-2222-4ccc-9ddd-000000000003
		/// H21, H25, H30, otro

table dFecha
	lineageTag: 3c3c3c3c-3333-4eee-afff-000000000001
	dataCategory: Time

	column Fecha
		dataType: dateTime
		isKey
		sourceColumn: fecha
		lineageTag: 3c3c3c3c-3333-4eee-afff-000000000002

	column Mes
		dataType: string
		sourceColumn: mes
		lineageTag: 3c3c3c3c-3333-4eee-afff-000000000003

table _Medidas
	lineageTag: 5d5d5d5d-4444-4fff-b000-000000000001

	measure 'Ventas Brutas' = SUM ( fVentas[Monto] )
		formatString: \\$#,0
		lineageTag: 5d5d5d5d-4444-4fff-b000-000000000002

	measure 'Ventas Netas' =
			CALCULATE (
				[Ventas Brutas],
				fVentas[Estado] = "ENTREGADO"
			)
		formatString: \\$#,0
		displayFolder: Ventas
		lineageTag: 5d5d5d5d-4444-4fff-b000-000000000003

	measure 'M3 Entregados' = CALCULATE ( SUM ( fVentas[M3] ), fVentas[Estado] = "ENTREGADO" )
		formatString: #,0.0
		lineageTag: 5d5d5d5d-4444-4fff-b000-000000000004

	measure 'Precio Promedio m3' = DIVIDE ( [Ventas Netas], [M3 Entregados] )
		formatString: \\$#,0.00
		lineageTag: 5d5d5d5d-4444-4fff-b000-000000000005

relationship a1b2c3d4-0001
	fromColumn: fVentas.IdCliente
	toColumn: dCliente.IdCliente

relationship a1b2c3d4-0002
	fromColumn: fVentas.IdProducto
	toColumn: dProducto.IdProducto

relationship a1b2c3d4-0003
	fromColumn: fVentas.Fecha
	toColumn: dFecha.Fecha
"""

# Lo que devuelve get_medida("Ventas Netas"): el objeto completo, como sale del modelo.
RESULTADO_GET_MEDIDA = {
    "nombre": "Ventas Netas",
    "tabla": "_Medidas",
    "expresion": 'CALCULATE ( [Ventas Brutas], fVentas[Estado] = "ENTREGADO" )',
    "dependencias": ["Ventas Brutas", "fVentas[Monto]", "fVentas[Estado]"],
    "formatString": "$#,0",
    "displayFolder": "Ventas",
    "isHidden": False,
    "dataType": "decimal",
    "lineageTag": "5d5d5d5d-4444-4fff-b000-000000000003",
    "description": None,
    "modifiedTime": "2026-09-30T14:22:07.113Z",
    "structureModifiedTime": "2026-09-30T14:22:07.113Z",
    "state": "ready",
    "errorMessage": None,
    "kpi": None,
    "detailRowsDefinition": None,
    "formatStringDefinition": None,
    "changedProperties": [{"property": "Expression"}, {"property": "FormatString"}, {"property": "DisplayFolder"}],
    "annotations": [
        {"name": "PBI_FormatHint", "value": '{"currencyCulture":"es-AR","isCustom":true}'},
        {"name": "TabularEditor_LastModifiedBy", "value": "rodo@hormigonera.com.ar"},
        {"name": "PBI_ChangedProperties", "value": "Expression,FormatString,DisplayFolder"},
    ],
    "extendedProperties": [
        {"name": "PBI_MeasureTemplate", "type": "json",
         "value": {"version": 0, "daxTemplateName": "Default", "parameters": []}},
    ],
}
