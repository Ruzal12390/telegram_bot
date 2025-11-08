# структура персонажа
player = {
	"name": "",
	"hp": 100,
	"armor": 0,
	"strenght": 0,
	"agility": 0,
	"charisma": 0,
	"intellect": 0,
	"inventory": []
}

equipment = [
	{
		"item_name": "Шлем бронзовый",
		"attribute": "armor",
		"value": 2,
	},
	{
		"item_name": "Деревянный щит",
		"attribute": "armor",
		"value": 3,
	},
	{
		"item_name": "Деревянный меч",
		"attribute": "strenght",
		"value": 5,
	}
]

enemies = [
	{
		"name": "Гоблин",
		"hp": 30,
		"armor": 2,
		"strenght": 5,
		"agility": 4,
		"charisma": 1,
		"intellect": 1,
		"inventory": []
	},
	{
		"name": "Лесной бандит",
		"hp": 50,
		"armor": 3,
		"strenght": 8,
		"agility": 6,
		"charisma": 2,
		"intellect": 3,
		"inventory": []
	},
]

npc = [
	{
		"name": "Тавернщик",
		"hp": 60,
		"armor": 1,
		"strenght": 2,
		"agility": 5,
		"charisma": 8,
		"intellect": 4,
		"inventory": [],
		"quests": []
	},
]