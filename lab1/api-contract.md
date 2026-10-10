# ЛР01. REST API-контракт

Базова адреса локальної реалізації ЛР2: http://127.0.0.1:8000. Обмін JSON UTF-8, Content-Type: application/json. Автентифікація та заголовки токенів відсутні. Усі приклади персональних даних синтетичні.

Нормативні бізнес-правила: [requirements.md](requirements.md), розділи 6–9. Відповідність назв прикладу методички (issues → requests, users → staff, priority → urgency) пояснено в requirements.md, розділ 2; додаткових альтернативних полів або маршрутів із попередніми назвами немає. Вичерпні JSON Schema Draft 2020-12 наведено в розділі 1 цього документа. Кожний підрозділ розділу 1 визначає один іменований елемент $defs: назва підрозділу — ключ, JSON-блок — значення. Для валідації зібрати ці визначення у $defs однієї кореневої схеми; $ref виду #/$defs/Request посилається на цей каталог. Окремі файли схем не потрібні. Схеми описують нормалізовані значення: спочатку trim за контрактом, потім minLength/maxLength. Дефолти застосовує сервер під час POST; PATCH їх не застосовує. Формати date/date-time перевіряються, а не лише документуються. Бізнес-залежності від збереженого стану та нерівність значень перевіряє service, не JSON Schema.

NoBody — позначення відсутнього HTTP-тіла, а не JSON null; ця схема не допускає жодного JSON-значення. У GET тіло не передається, у маршрутах без {id} path-параметрів немає. Неописані query-параметри — 422, body в GET — 422. JSON path/query у схемах є нормалізованим поданням параметрів: path "1" розбирається як 1; "abc", 0 і від’ємне — 422. Enum query case-sensitive; повтор одного query-ключа — 422 (уточнення для однозначності фільтра). Непідтримувані HTTP method та невідомі URL мають стандартну транспортну відповідь 405/404 і не є бізнес-сценаріями цього контракту.

Успішні відповіді на GET/PATCH/close — 200, створення звернення та коментаря — 201. Усі бізнес-помилки мають схему Error. Не виконуються жодні зміни до успішної повної перевірки. Пріоритет перевірок задано в requirements.md §8–9.

## 1. Каталог JSON-схем

### Staff

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "enum": [
        1,
        2
      ]
    },
    "name": {
      "type": "string",
      "enum": [
        "Agent A",
        "Agent B"
      ]
    }
  },
  "required": [
    "id",
    "name"
  ],
  "additionalProperties": false,
  "oneOf": [
    {
      "properties": {
        "id": {
          "const": 1
        },
        "name": {
          "const": "Agent A"
        }
      }
    },
    {
      "properties": {
        "id": {
          "const": 2
        },
        "name": {
          "const": "Agent B"
        }
      }
    }
  ]
}
```

### CertificateDetails

```json
{
  "type": "object",
  "properties": {
    "language": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "uk",
            "en"
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "purpose": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 3,
          "maxLength": 200
        },
        {
          "type": "null"
        }
      ]
    },
    "delivery_method": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "digital",
            "physical"
          ]
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [],
  "additionalProperties": false
}
```

### CorrectionDetails

```json
{
  "type": "object",
  "properties": {
    "target_field": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 64
        },
        {
          "type": "null"
        }
      ]
    },
    "current_value": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        },
        {
          "type": "null"
        }
      ]
    },
    "proposed_value": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [],
  "additionalProperties": false
}
```

### CertificateResult

```json
{
  "type": "object",
  "properties": {
    "certificate_number": {
      "type": "string",
      "minLength": 1,
      "maxLength": 64
    },
    "issued_on": {
      "type": "string",
      "format": "date"
    }
  },
  "required": [
    "certificate_number",
    "issued_on"
  ],
  "additionalProperties": false
}
```

### CorrectionResult

```json
{
  "type": "object",
  "properties": {
    "target_field": {
      "type": "string",
      "minLength": 1,
      "maxLength": 64
    },
    "previous_value": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "corrected_value": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "corrected_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": [
    "target_field",
    "previous_value",
    "corrected_value",
    "corrected_at"
  ],
  "additionalProperties": false
}
```

### ResolutionInput

```json
{
  "type": "object",
  "properties": {
    "resolution_code": {
      "type": "string",
      "enum": [
        "COMPLETED",
        "REJECTED"
      ]
    },
    "result_details": {
      "anyOf": [
        {
          "oneOf": [
            {
              "$ref": "#/$defs/CertificateResult"
            },
            {
              "$ref": "#/$defs/CorrectionResult"
            }
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "rejection_reason": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 10,
          "maxLength": 2000
        },
        {
          "type": "null"
        }
      ]
    },
    "resolved_by": {
      "type": "integer",
      "enum": [
        1,
        2
      ]
    }
  },
  "required": [
    "resolution_code",
    "resolved_by"
  ],
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "resolution_code": {
            "const": "COMPLETED"
          }
        }
      },
      "then": {
        "required": [
          "result_details"
        ],
        "properties": {
          "result_details": {
            "oneOf": [
              {
                "$ref": "#/$defs/CertificateResult"
              },
              {
                "$ref": "#/$defs/CorrectionResult"
              }
            ]
          },
          "rejection_reason": {
            "type": "null"
          }
        }
      },
      "else": {
        "required": [
          "rejection_reason"
        ],
        "properties": {
          "rejection_reason": {
            "type": "string",
            "minLength": 10,
            "maxLength": 2000
          },
          "result_details": {
            "type": "null"
          }
        }
      }
    }
  ]
}
```

### Resolution

```json
{
  "type": "object",
  "properties": {
    "resolution_code": {
      "type": "string",
      "enum": [
        "COMPLETED",
        "REJECTED"
      ]
    },
    "result_details": {
      "anyOf": [
        {
          "oneOf": [
            {
              "$ref": "#/$defs/CertificateResult"
            },
            {
              "$ref": "#/$defs/CorrectionResult"
            }
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "rejection_reason": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 10,
          "maxLength": 2000
        },
        {
          "type": "null"
        }
      ]
    },
    "resolved_by": {
      "type": "integer",
      "enum": [
        1,
        2
      ]
    },
    "resolved_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": [
    "resolution_code",
    "result_details",
    "rejection_reason",
    "resolved_by",
    "resolved_at"
  ],
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "resolution_code": {
            "const": "COMPLETED"
          }
        }
      },
      "then": {
        "required": [
          "result_details"
        ],
        "properties": {
          "result_details": {
            "oneOf": [
              {
                "$ref": "#/$defs/CertificateResult"
              },
              {
                "$ref": "#/$defs/CorrectionResult"
              }
            ]
          },
          "rejection_reason": {
            "type": "null"
          }
        }
      },
      "else": {
        "required": [
          "rejection_reason"
        ],
        "properties": {
          "rejection_reason": {
            "type": "string",
            "minLength": 10,
            "maxLength": 2000
          },
          "result_details": {
            "type": "null"
          }
        }
      }
    }
  ]
}
```

### Completeness

```json
{
  "type": "object",
  "properties": {
    "type_confirmed": {
      "type": "boolean"
    },
    "is_complete": {
      "type": "boolean"
    },
    "missing_fields": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    }
  },
  "required": [
    "type_confirmed",
    "is_complete",
    "missing_fields"
  ],
  "additionalProperties": false
}
```

### RequestCreate

```json
{
  "type": "object",
  "properties": {
    "student_id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 32
    },
    "full_name": {
      "type": "string",
      "minLength": 3,
      "maxLength": 120
    },
    "title": {
      "type": "string",
      "minLength": 3,
      "maxLength": 120
    },
    "description": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2000,
      "default": ""
    },
    "urgency": {
      "type": "string",
      "enum": [
        "low",
        "medium",
        "high"
      ],
      "default": "medium"
    },
    "assignee_id": {
      "anyOf": [
        {
          "type": "integer",
          "enum": [
            1,
            2
          ]
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "certificate_details": {
      "anyOf": [
        {
          "$ref": "#/$defs/CertificateDetails",
          "minProperties": 1
        },
        {
          "type": "null"
        }
      ]
    },
    "correction_details": {
      "anyOf": [
        {
          "$ref": "#/$defs/CorrectionDetails",
          "minProperties": 1
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "student_id",
    "full_name",
    "title"
  ],
  "additionalProperties": false,
  "allOf": [
    {
      "not": {
        "required": [
          "certificate_details",
          "correction_details"
        ],
        "properties": {
          "certificate_details": {
            "type": "object"
          },
          "correction_details": {
            "type": "object"
          }
        }
      }
    }
  ]
}
```

### RequestPatch

```json
{
  "type": "object",
  "properties": {
    "student_id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 32
    },
    "full_name": {
      "type": "string",
      "minLength": 3,
      "maxLength": 120
    },
    "title": {
      "type": "string",
      "minLength": 3,
      "maxLength": 120
    },
    "description": {
      "type": "string",
      "maxLength": 2000
    },
    "urgency": {
      "type": "string",
      "enum": [
        "low",
        "medium",
        "high"
      ]
    },
    "assignee_id": {
      "anyOf": [
        {
          "type": "integer",
          "enum": [
            1,
            2
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "certificate_details": {
      "anyOf": [
        {
          "$ref": "#/$defs/CertificateDetails"
        },
        {
          "type": "null"
        }
      ]
    },
    "correction_details": {
      "anyOf": [
        {
          "$ref": "#/$defs/CorrectionDetails"
        },
        {
          "type": "null"
        }
      ]
    },
    "request_type": {
      "type": "string",
      "enum": [
        "ENROLLMENT_CERTIFICATE",
        "STUDENT_DATA_CORRECTION"
      ]
    },
    "type_confirmed_by": {
      "type": "integer",
      "enum": [
        1,
        2
      ]
    }
  },
  "required": [],
  "additionalProperties": false,
  "dependentRequired": {
    "request_type": [
      "type_confirmed_by"
    ],
    "type_confirmed_by": [
      "request_type"
    ]
  }
}
```

### Request

```json
{
  "type": "object",
  "properties": {
    "student_id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 32
    },
    "full_name": {
      "type": "string",
      "minLength": 3,
      "maxLength": 120
    },
    "title": {
      "type": "string",
      "minLength": 3,
      "maxLength": 120
    },
    "description": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2000,
      "default": ""
    },
    "urgency": {
      "type": "string",
      "enum": [
        "low",
        "medium",
        "high"
      ],
      "default": "medium"
    },
    "assignee_id": {
      "anyOf": [
        {
          "type": "integer",
          "enum": [
            1,
            2
          ]
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "certificate_details": {
      "anyOf": [
        {
          "$ref": "#/$defs/CertificateDetailsResponse"
        },
        {
          "type": "null"
        }
      ]
    },
    "correction_details": {
      "anyOf": [
        {
          "$ref": "#/$defs/CorrectionDetailsResponse"
        },
        {
          "type": "null"
        }
      ]
    },
    "id": {
      "type": "integer",
      "minimum": 1
    },
    "status": {
      "type": "string",
      "enum": [
        "OPEN",
        "IN_PROGRESS",
        "CLOSED"
      ]
    },
    "request_type": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "ENROLLMENT_CERTIFICATE",
            "STUDENT_DATA_CORRECTION"
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "type_confirmed_by": {
      "anyOf": [
        {
          "type": "integer",
          "enum": [
            1,
            2
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "type_confirmed_at": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ]
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "resolution": {
      "anyOf": [
        {
          "$ref": "#/$defs/Resolution"
        },
        {
          "type": "null"
        }
      ]
    },
    "completeness": {
      "$ref": "#/$defs/Completeness"
    }
  },
  "required": [
    "student_id",
    "full_name",
    "title",
    "description",
    "urgency",
    "assignee_id",
    "certificate_details",
    "correction_details",
    "id",
    "status",
    "request_type",
    "type_confirmed_by",
    "type_confirmed_at",
    "created_at",
    "resolution",
    "completeness"
  ],
  "additionalProperties": false
}
```

### StatusPatch

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": [
        "OPEN",
        "IN_PROGRESS",
        "CLOSED"
      ]
    },
    "resolution": {
      "$ref": "#/$defs/ResolutionInput"
    }
  },
  "required": [
    "status"
  ],
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "status": {
            "enum": [
              "OPEN",
              "IN_PROGRESS"
            ]
          }
        }
      },
      "then": {
        "not": {
          "required": [
            "resolution"
          ]
        }
      }
    }
  ]
}
```

### CloseInput

```json
{
  "type": "object",
  "properties": {
    "resolution": {
      "$ref": "#/$defs/ResolutionInput"
    }
  },
  "required": [
    "resolution"
  ],
  "additionalProperties": false
}
```

### CommentCreate

```json
{
  "type": "object",
  "properties": {
    "author_id": {
      "type": "integer",
      "enum": [
        1,
        2
      ]
    },
    "text": {
      "type": "string",
      "minLength": 1,
      "maxLength": 1000
    }
  },
  "required": [
    "author_id",
    "text"
  ],
  "additionalProperties": false
}
```

### Comment

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1
    },
    "request_id": {
      "type": "integer",
      "minimum": 1
    },
    "author_id": {
      "type": "integer",
      "enum": [
        1,
        2
      ]
    },
    "text": {
      "type": "string",
      "minLength": 1,
      "maxLength": 1000
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": [
    "id",
    "request_id",
    "author_id",
    "text",
    "created_at"
  ],
  "additionalProperties": false
}
```

### AIRecommendation

```json
{
  "type": "object",
  "properties": {
    "recommended_type": {
      "type": "string",
      "enum": [
        "ENROLLMENT_CERTIFICATE",
        "STUDENT_DATA_CORRECTION"
      ]
    },
    "recommended_urgency": {
      "type": "string",
      "enum": [
        "low",
        "medium",
        "high"
      ]
    },
    "summary": {
      "type": "string",
      "minLength": 1,
      "maxLength": 500
    },
    "completeness_hint": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 1000
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "recommended_type",
    "recommended_urgency",
    "summary",
    "completeness_hint"
  ],
  "additionalProperties": false,
  "description": "Після підтвердження типу service вимагає непорожній completeness_hint; до підтвердження дозволено null. Перевірка залежить від snapshot і виконується у ЛР4."
}
```

### Error

```json
{
  "type": "object",
  "properties": {
    "error": {
      "type": "object",
      "properties": {
        "code": {
          "type": "string"
        },
        "message": {
          "type": "string"
        },
        "details": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "field": {
                "type": "string"
              },
              "reason": {
                "type": "string"
              }
            },
            "required": [
              "field",
              "reason"
            ],
            "additionalProperties": false
          }
        }
      },
      "required": [
        "code",
        "message",
        "details"
      ],
      "additionalProperties": false
    }
  },
  "required": [
    "error"
  ],
  "additionalProperties": false
}
```

### Health

```json
{
  "type": "object",
  "properties": {
    "status": {
      "const": "ok"
    }
  },
  "required": [
    "status"
  ],
  "additionalProperties": false
}
```

### StaffList

```json
{
  "type": "array",
  "items": {
    "$ref": "#/$defs/Staff"
  },
  "minItems": 2,
  "maxItems": 2
}
```

### RequestList

```json
{
  "type": "array",
  "items": {
    "$ref": "#/$defs/Request"
  }
}
```

### CommentList

```json
{
  "type": "array",
  "items": {
    "$ref": "#/$defs/Comment"
  }
}
```

### NoBody

```json
{
  "not": {}
}
```

### CertificateDetailsResponse

```json
{
  "type": "object",
  "properties": {
    "language": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "uk",
            "en"
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "purpose": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 3,
          "maxLength": 200
        },
        {
          "type": "null"
        }
      ]
    },
    "delivery_method": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "digital",
            "physical"
          ]
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "language",
    "purpose",
    "delivery_method"
  ],
  "additionalProperties": false
}
```

### CorrectionDetailsResponse

```json
{
  "type": "object",
  "properties": {
    "target_field": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 64
        },
        {
          "type": "null"
        }
      ]
    },
    "current_value": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        },
        {
          "type": "null"
        }
      ]
    },
    "proposed_value": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "target_field",
    "current_value",
    "proposed_value"
  ],
  "additionalProperties": false
}
```

## 2. Контракти всіх 10 маршрутів

### 2.1. GET /health

Технічна перевірка процесу без звернення до LLM. Не є гарантією комплектності даних чи виконаної студентської послуги.

**Path schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/NoBody"
}
```

**Приклад запиту:** GET /health

Тіло відсутнє.

**Успіх: 200. Схема відповіді:**

```json
{
  "$ref": "#/$defs/Health"
}
```

**Повне тіло відповіді:**

```json
{
  "status": "ok"
}
```

**Контрактні помилки:** 422 при зайвих параметрах або тілі GET; доменних 400/404/409 для цього маршруту немає.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні параметри запиту",
    "details": [
      {
        "field": "query.foo",
        "reason": "Невідомий параметр."
      }
    ]
  }
}
```

---

### 2.2. GET /staff

Незмінний довідник, порядок id ASC; створення, редагування та видалення співробітників відсутні.

**Path schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/NoBody"
}
```

**Приклад запиту:** GET /staff

Тіло відсутнє.

**Успіх: 200. Схема відповіді:**

```json
{
  "$ref": "#/$defs/StaffList"
}
```

**Повне тіло відповіді:**

```json
[
  {
    "id": 1,
    "name": "Agent A"
  },
  {
    "id": 2,
    "name": "Agent B"
  }
]
```

**Контрактні помилки:** 422 при зайвих параметрах або тілі GET; доменних 400/404/409 для цього маршруту немає.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні параметри запиту",
    "details": [
      {
        "field": "query.foo",
        "reason": "Невідомий параметр."
      }
    ]
  }
}
```

---

### 2.3. POST /requests

Створення лише OPEN. Тип підтверджується пізніше. Сервер не приймає id/status/request_type/type_confirmed_by/created_at. Початкові неповні реквізити одного виду дозволені; порожній об’єкт деталей — 422. У відповіді ненульовий об’єкт реквізитів містить усі свої поля, пропущені при створенні нормалізуються до null.

**Path schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/RequestCreate"
}
```

**Приклад запиту:** POST /requests

```json
{
  "student_id": "S-2308001",
  "full_name": "Тестовий Студент",
  "title": "Довідка про навчання",
  "description": "Потрібна довідка для подання за місцем вимоги."
}
```

**Успіх: 201. Схема відповіді:**

```json
{
  "$ref": "#/$defs/Request"
}
```

**Повне тіло відповіді:**

```json
{
  "id": 1,
  "student_id": "S-2308001",
  "full_name": "Тестовий Студент",
  "title": "Довідка про навчання",
  "description": "Потрібна довідка для подання за місцем вимоги.",
  "urgency": "medium",
  "status": "OPEN",
  "assignee_id": null,
  "request_type": null,
  "type_confirmed_by": null,
  "type_confirmed_at": null,
  "certificate_details": null,
  "correction_details": null,
  "created_at": "2026-10-10T10:00:00Z",
  "resolution": null,
  "completeness": {
    "type_confirmed": false,
    "is_complete": false,
    "missing_fields": [
      "request_type"
    ]
  }
}
```

**Помилки та повні приклади:**

**422:** Невалідні параметри/JSON, відсутнє required, null non-null, unknown field, неправильний enum чи межі. Для status=CLOSED без resolution при фактичному переході також 422.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні дані запиту.",
    "details": [
      {
        "field": "body.title",
        "reason": "Після trim потрібно від 3 до 120 символів."
      }
    ]
  }
}
```

---

### 2.4. GET /requests

Фільтри з query застосовуються AND; відсутній фільтр не обмежує результати. request_type фільтрує лише підтверджене поле. Без збігів — []. Приклад: /requests?status=OPEN&urgency=medium&request_type=ENROLLMENT_CERTIFICATE.

**Path schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": [
        "OPEN",
        "IN_PROGRESS",
        "CLOSED"
      ]
    },
    "urgency": {
      "type": "string",
      "enum": [
        "low",
        "medium",
        "high"
      ]
    },
    "request_type": {
      "type": "string",
      "enum": [
        "ENROLLMENT_CERTIFICATE",
        "STUDENT_DATA_CORRECTION"
      ]
    }
  },
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/NoBody"
}
```

**Приклад запиту:** GET /requests

Тіло відсутнє.

**Успіх: 200. Схема відповіді:**

```json
{
  "$ref": "#/$defs/RequestList"
}
```

**Повне тіло відповіді:**

```json
[
  {
    "id": 1,
    "student_id": "S-2308001",
    "full_name": "Тестовий Студент",
    "title": "Довідка про навчання",
    "description": "Потрібна довідка для подання за місцем вимоги.",
    "urgency": "medium",
    "status": "OPEN",
    "assignee_id": null,
    "request_type": "ENROLLMENT_CERTIFICATE",
    "type_confirmed_by": 1,
    "type_confirmed_at": "2026-10-10T10:05:00Z",
    "certificate_details": {
      "language": "uk",
      "purpose": "За місцем вимоги",
      "delivery_method": "digital"
    },
    "correction_details": null,
    "created_at": "2026-10-10T10:00:00Z",
    "resolution": null,
    "completeness": {
      "type_confirmed": true,
      "is_complete": true,
      "missing_fields": []
    }
  }
]
```

**Помилки та повні приклади:**

**422:** Неправильний path/query, зайві параметри або тіло GET.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні дані запиту.",
    "details": [
      {
        "field": "query.urgency",
        "reason": "Допустимі low, medium, high."
      }
    ]
  }
}
```

---

### 2.5. GET /requests/{id}

Повертає весь Request, включаючи реквізити, completeness та resolution. Коментарі отримуються окремо. Ідентифікатор прикладу — 1.

**Path schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/NoBody"
}
```

**Приклад запиту:** GET /requests/1

Тіло відсутнє.

**Успіх: 200. Схема відповіді:**

```json
{
  "$ref": "#/$defs/Request"
}
```

**Повне тіло відповіді:**

```json
{
  "id": 1,
  "student_id": "S-2308001",
  "full_name": "Тестовий Студент",
  "title": "Довідка про навчання",
  "description": "Потрібна довідка для подання за місцем вимоги.",
  "urgency": "medium",
  "status": "OPEN",
  "assignee_id": null,
  "request_type": "ENROLLMENT_CERTIFICATE",
  "type_confirmed_by": 1,
  "type_confirmed_at": "2026-10-10T10:05:00Z",
  "certificate_details": {
    "language": "uk",
    "purpose": "За місцем вимоги",
    "delivery_method": "digital"
  },
  "correction_details": null,
  "created_at": "2026-10-10T10:00:00Z",
  "resolution": null,
  "completeness": {
    "type_confirmed": true,
    "is_complete": true,
    "missing_fields": []
  }
}
```

**Помилки та повні приклади:**

**404:** Валідний id=999 не існує.

```json
{
  "error": {
    "code": "REQUEST_NOT_FOUND",
    "message": "Звернення з id=999 не знайдено.",
    "details": []
  }
}
```

**422:** Неправильний path/query, зайві параметри або тіло GET.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні дані запиту.",
    "details": [
      {
        "field": "path.id",
        "reason": "Потрібне додатне ціле число."
      }
    ]
  }
}
```

---

### 2.6. PATCH /requests/{id}

Повна семантика PATCH — requirements.md §8. Приклад підтверджує тип і доповнює реквізити OPEN атомарно. Статус не змінюється.

**Path schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/RequestPatch"
}
```

**Приклад запиту:** PATCH /requests/1

```json
{
  "request_type": "ENROLLMENT_CERTIFICATE",
  "type_confirmed_by": 1,
  "certificate_details": {
    "language": "uk",
    "purpose": "За місцем вимоги",
    "delivery_method": "digital"
  }
}
```

**Успіх: 200. Схема відповіді:**

```json
{
  "$ref": "#/$defs/Request"
}
```

**Повне тіло відповіді:**

```json
{
  "id": 1,
  "student_id": "S-2308001",
  "full_name": "Тестовий Студент",
  "title": "Довідка про навчання",
  "description": "Потрібна довідка для подання за місцем вимоги.",
  "urgency": "medium",
  "status": "OPEN",
  "assignee_id": null,
  "request_type": "ENROLLMENT_CERTIFICATE",
  "type_confirmed_by": 1,
  "type_confirmed_at": "2026-10-10T10:05:00Z",
  "certificate_details": {
    "language": "uk",
    "purpose": "За місцем вимоги",
    "delivery_method": "digital"
  },
  "correction_details": null,
  "created_at": "2026-10-10T10:00:00Z",
  "resolution": null,
  "completeness": {
    "type_confirmed": true,
    "is_complete": true,
    "missing_fields": []
  }
}
```

**Помилки та повні приклади:**

**400:** Порожній об’єкт PATCH або порожній вкладений об’єкт.

```json
{
  "error": {
    "code": "EMPTY_PATCH",
    "message": "Не передано жодної зміни.",
    "details": [
      {
        "field": "body",
        "reason": "Передайте хоча б одне поле; вкладений об’єкт не може бути порожнім."
      }
    ]
  }
}
```

**404:** Валідний id=999 не існує.

```json
{
  "error": {
    "code": "REQUEST_NOT_FOUND",
    "message": "Звернення з id=999 не знайдено.",
    "details": []
  }
}
```

**409:** CLOSED; TYPE_LOCKED для зміни типу/автора IN_PROGRESS; REQUEST_INCOMPLETE для втрати реквізитів у IN_PROGRESS.

```json
{
  "error": {
    "code": "REQUEST_CLOSED",
    "message": "Закрите звернення не редагується.",
    "details": [
      {
        "field": "request.status",
        "reason": "Статус CLOSED є фінальним."
      }
    ]
  }
}
```

**422:** Невалідні параметри/JSON, відсутнє required, null non-null, unknown field, неправильний enum чи межі. Для status=CLOSED без resolution при фактичному переході також 422.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні дані запиту.",
    "details": [
      {
        "field": "body.assignee_id",
        "reason": "Допустимі 1, 2 або null."
      }
    ]
  }
}
```

---

### 2.7. PATCH /requests/{id}/status

Статус за матрицею requirements.md §7. Для реального переходу в CLOSED потрібна resolution в тому самому тілі; для повтору CLOSED вона необов’язкова. Для інших status резолюція заборонена. Цю залежність поточного стану перевіряє service.

**Path schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/StatusPatch"
}
```

**Приклад запиту:** PATCH /requests/1/status

```json
{
  "status": "IN_PROGRESS"
}
```

**Успіх: 200. Схема відповіді:**

```json
{
  "$ref": "#/$defs/Request"
}
```

**Повне тіло відповіді:**

```json
{
  "id": 1,
  "student_id": "S-2308001",
  "full_name": "Тестовий Студент",
  "title": "Довідка про навчання",
  "description": "Потрібна довідка для подання за місцем вимоги.",
  "urgency": "medium",
  "status": "IN_PROGRESS",
  "assignee_id": null,
  "request_type": "ENROLLMENT_CERTIFICATE",
  "type_confirmed_by": 1,
  "type_confirmed_at": "2026-10-10T10:05:00Z",
  "certificate_details": {
    "language": "uk",
    "purpose": "За місцем вимоги",
    "delivery_method": "digital"
  },
  "correction_details": null,
  "created_at": "2026-10-10T10:00:00Z",
  "resolution": null,
  "completeness": {
    "type_confirmed": true,
    "is_complete": true,
    "missing_fields": []
  }
}
```

**Помилки та повні приклади:**

**404:** Валідний id=999 не існує.

```json
{
  "error": {
    "code": "REQUEST_NOT_FOUND",
    "message": "Звернення з id=999 не знайдено.",
    "details": []
  }
}
```

**409:** IN_PROGRESS для неповного підтвердженого типу; TYPE_NOT_CONFIRMED без підтвердження; INVALID_TRANSITION для зворотних переходів; RESULT_MISMATCH або RESOLUTION_CONFLICT при закритті.

```json
{
  "error": {
    "code": "REQUEST_INCOMPLETE",
    "message": "Для початку обробки бракує даних.",
    "details": [
      {
        "field": "request.certificate_details.purpose",
        "reason": "Обов’язкове поле не заповнено."
      }
    ]
  }
}
```

**422:** Невалідні параметри/JSON, відсутнє required, null non-null, unknown field, неправильний enum чи межі. Для status=CLOSED без resolution при фактичному переході також 422.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні дані запиту.",
    "details": [
      {
        "field": "body.status",
        "reason": "Допустимі OPEN, IN_PROGRESS, CLOSED."
      }
    ]
  }
}
```

---

### 2.8. POST /requests/{id}/close

Еквівалент PATCH status=CLOSED із резолюцією. Обидва маршрути використовують один use case close_request, одну транзакцію та однакові бізнес-помилки. Для REJECTED completeness не є умовою.

**Path schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/CloseInput"
}
```

**Приклад запиту:** POST /requests/1/close

```json
{
  "resolution": {
    "resolution_code": "COMPLETED",
    "result_details": {
      "certificate_number": "CERT-2026-001",
      "issued_on": "2026-10-10"
    },
    "rejection_reason": null,
    "resolved_by": 1
  }
}
```

**Успіх: 200. Схема відповіді:**

```json
{
  "$ref": "#/$defs/Request"
}
```

**Повне тіло відповіді:**

```json
{
  "id": 1,
  "student_id": "S-2308001",
  "full_name": "Тестовий Студент",
  "title": "Довідка про навчання",
  "description": "Потрібна довідка для подання за місцем вимоги.",
  "urgency": "medium",
  "status": "CLOSED",
  "assignee_id": null,
  "request_type": "ENROLLMENT_CERTIFICATE",
  "type_confirmed_by": 1,
  "type_confirmed_at": "2026-10-10T10:05:00Z",
  "certificate_details": {
    "language": "uk",
    "purpose": "За місцем вимоги",
    "delivery_method": "digital"
  },
  "correction_details": null,
  "created_at": "2026-10-10T10:00:00Z",
  "resolution": {
    "resolution_code": "COMPLETED",
    "result_details": {
      "certificate_number": "CERT-2026-001",
      "issued_on": "2026-10-10"
    },
    "rejection_reason": null,
    "resolved_by": 1,
    "resolved_at": "2026-10-10T10:15:00Z"
  },
  "completeness": {
    "type_confirmed": true,
    "is_complete": true,
    "missing_fields": []
  }
}
```

**Помилки та повні приклади:**

**404:** Валідний id=999 не існує.

```json
{
  "error": {
    "code": "REQUEST_NOT_FOUND",
    "message": "Звернення з id=999 не знайдено.",
    "details": []
  }
}
```

**409:** COMPLETED без підтвердження/комплектності; RESULT_MISMATCH при іншому типі результату; RESOLUTION_CONFLICT при зміні вже збереженого результату.

```json
{
  "error": {
    "code": "TYPE_NOT_CONFIRMED",
    "message": "Не можна зафіксувати виконання без підтвердженого типу.",
    "details": [
      {
        "field": "request.request_type",
        "reason": "Підтвердьте тип співробітником."
      }
    ]
  }
}
```

**422:** Невалідні параметри/JSON, відсутнє required, null non-null, unknown field, неправильний enum чи межі. Для status=CLOSED без resolution при фактичному переході також 422.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні дані запиту.",
    "details": [
      {
        "field": "body.resolution.rejection_reason",
        "reason": "Для REJECTED потрібно від 10 до 2000 символів."
      }
    ]
  }
}
```

---

### 2.9. POST /requests/{id}/comments

Коментар дозволений у CLOSED. Не змінює реквізитів або completeness. request_id/id/created_at із body заборонені.

**Path schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/CommentCreate"
}
```

**Приклад запиту:** POST /requests/1/comments

```json
{
  "author_id": 2,
  "text": "Уточніть призначення довідки."
}
```

**Успіх: 201. Схема відповіді:**

```json
{
  "$ref": "#/$defs/Comment"
}
```

**Повне тіло відповіді:**

```json
{
  "id": 1,
  "request_id": 1,
  "author_id": 2,
  "text": "Уточніть призначення довідки.",
  "created_at": "2026-10-10T10:02:00Z"
}
```

**Помилки та повні приклади:**

**404:** Валідний id=999 не існує.

```json
{
  "error": {
    "code": "REQUEST_NOT_FOUND",
    "message": "Звернення з id=999 не знайдено.",
    "details": []
  }
}
```

**422:** Невалідні параметри/JSON, відсутнє required, null non-null, unknown field, неправильний enum чи межі. Для status=CLOSED без resolution при фактичному переході також 422.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні дані запиту.",
    "details": [
      {
        "field": "body.text",
        "reason": "Після trim потрібно від 1 до 1000 символів."
      }
    ]
  }
}
```

---

### 2.10. GET /requests/{id}/comments

Порядок created_at ASC, id ASC. Наявне звернення без коментарів — 200 та []; відсутнє звернення — 404.

**Path schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

**Query schema:**

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

**JSON Schema тіла запиту:**

```json
{
  "$ref": "#/$defs/NoBody"
}
```

**Приклад запиту:** GET /requests/1/comments

Тіло відсутнє.

**Успіх: 200. Схема відповіді:**

```json
{
  "$ref": "#/$defs/CommentList"
}
```

**Повне тіло відповіді:**

```json
[
  {
    "id": 1,
    "request_id": 1,
    "author_id": 2,
    "text": "Уточніть призначення довідки.",
    "created_at": "2026-10-10T10:02:00Z"
  }
]
```

**Помилки та повні приклади:**

**404:** Валідний id=999 не існує.

```json
{
  "error": {
    "code": "REQUEST_NOT_FOUND",
    "message": "Звернення з id=999 не знайдено.",
    "details": []
  }
}
```

**422:** Неправильний path/query, зайві параметри або тіло GET.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні дані запиту.",
    "details": [
      {
        "field": "path.id",
        "reason": "Потрібне додатне ціле число."
      }
    ]
  }
}
```

---

## 3. Додаткові приклади бізнес-помилок

### CLOSED → OPEN

Запит PATCH /requests/1/status, тіло {"status":"OPEN"} для CLOSED. Відповідь 409:

```json
{
  "error": {
    "code": "INVALID_TRANSITION",
    "message": "Перехід CLOSED → OPEN заборонений.",
    "details": [
      {
        "field": "request.status",
        "reason": "Фінальний стан не змінюється."
      }
    ]
  }
}
```

### Спроба початку без підтвердження

Запит PATCH /requests/1/status, тіло {"status":"IN_PROGRESS"} для непідтвердженого OPEN. Відповідь 409:

```json
{
  "error": {
    "code": "TYPE_NOT_CONFIRMED",
    "message": "Тип звернення не підтверджено.",
    "details": [
      {
        "field": "request.request_type",
        "reason": "Передайте request_type і type_confirmed_by через PATCH звернення."
      }
    ]
  }
}
```

### Частково невалідний PATCH

Запит PATCH /requests/1, тіло {"title":"Нова назва","urgency":"HIGH"}. Відповідь 422; жодної зміни title:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Некоректні дані запиту.",
    "details": [
      {
        "field": "body.urgency",
        "reason": "Допустимі low, medium, high."
      }
    ]
  }
}
```

### Відмова без підтвердженого типу

POST /requests/1/close для OPEN допускає таке тіло:

```json
{
  "resolution": {
    "resolution_code": "REJECTED",
    "rejection_reason": "Заявлена послуга не надається цим підрозділом.",
    "resolved_by": 2
  }
}
```

Відповідь 200 має повну Request зі status=CLOSED, resolution.result_details=null та серверним resolved_at; completeness лишається false. Повна структура Request наведена в розділі 1, успішні повні приклади закриття — в контрактах маршрутів.

### Виконане виправлення

Для підтвердженого комплектного STUDENT_DATA_CORRECTION із target_field="full_name", current_value="Тестова Помилка", proposed_value="Тестове Ім’я" команда закриття:

```json
{
  "resolution": {
    "resolution_code": "COMPLETED",
    "result_details": {
      "target_field": "full_name",
      "previous_value": "Тестова Помилка",
      "corrected_value": "Тестове Ім’я",
      "corrected_at": "2026-10-10T10:14:00Z"
    },
    "resolved_by": 1
  }
}
```

Форма валідна; відповідь 200 зі збереженим результатом. Якщо corrected_value відрізняється від proposed_value, 409 RESULT_MISMATCH з field=body.resolution.result_details.corrected_value, без зміни статусу та резолюції.

## 4. Узгодженість двох способів закриття

PATCH status із status=CLOSED та повною resolution і POST close із повною resolution є двома входами одного use case. Нормативні повні схеми та конкретні тіла наведені вище. При повторі закриття порівнюються всі нормалізовані користувацькі поля резолюції; відсутні nullable поля нормалізуються до null; resolved_at у вхідних даних заборонений. Рівний повтор не змінює жодних значень або часу.
