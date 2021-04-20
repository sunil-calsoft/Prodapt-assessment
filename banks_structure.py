banks_structure = {"bank1":
   {
      "type": "csv",
      "fields":
      [
         {
            "name": "timestamp",
            "type": "date",
            "format":"%b %d %Y"
         },
         {
            "name": "type",
            "type": "string"
         },
         {
            "name": "amount",
            "type": "float"
         },
         {
            "name": "from",
            "type": "int"
         },
         {
            "name": "to",
            "type": "int"
         }
      ],
      "to_csv":
      [
         {
            "name": "date",
            "field": "timestamp"
         },
         {
            "name": "type",
            "field": "type"
         },
         {
            "name": "amount",
            "field": "amount"
         },
         {
            "name": "from",
            "field": "from"
         },
         {
            "name": "to",
            "field": "to"
         }
      ]
   },
   "bank2":
   {
      "type": "csv",
      "fields":
      [
         {
            "name": "date",
            "type": "date",
            "format":"%d-%m-%Y"
         },
         {
            "name": "transaction",
            "type": "string"
         },
         {
            "name": "amounts",
            "type": "float"
         },
         {
            "name": "to",
            "type": "int"
         },
         {
            "name": "from",
            "type": "int"
         }
      ],
      "to_csv":
      [
         {
            "name": "date",
            "field": "date"
         },
         {
            "name": "type",
            "field": "transaction"
         },
         {
            "name": "amount",
            "field": "amounts"
         },
         {
            "name": "from",
            "field": "from"
         },
         {
            "name": "to",
            "field": "to"
         }
      ]
   },
   "bank3":
   {
      "type": "csv",
      "fields":
      [
         {
            "name": "date_readable",
            "type": "date",
            "format":"%d %b %Y"
         },
         {
            "name": "type",
            "type": "string"
         },
         {
            "name": "euro",
            "type": "int"
         },
         {
            "name": "cents",
            "type": "int"
         },
         {
            "name": "to",
            "type": "int"
         },
         {
            "name": "from",
            "type": "int"
         }
      ],
      "transform":
      [
            ["divide", "cents", 100],
            ["add_fields", "euro", "cents"]
      ],
      "to_csv":
      [
         {
            "name": "date",
            "field": "date_readable"
         },
         {
            "name": "type",
            "field": "type"
         },
         {
            "name": "amount",
            "field": "euro"
         },
         {
            "name": "from",
            "field": "from"
         },
         {
            "name": "to",
            "field": "to"
         }
      ]
   }
}