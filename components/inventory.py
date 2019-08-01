from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.equipment = []
        self.owner = None

    def add_item(self, item_entity):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                "item_added":
                None,
                "message":
                Message(
                    "You cannot carry any more items, your backpack is full.",
                    "yellow")
            })
        elif len(self.equipment) >= self.capacity:
            results.append({
                "item_added":
                None,
                "message":
                Message(
                    "You cannot carry any more equipment, your inventory is full.",
                    "yellow")
            })
        elif item_entity.item and not item_entity.equippable:
            for inventory_item in self.items:
                if inventory_item.name == item_entity.name:
                    inventory_item.item.quantity += item_entity.item.quantity
                    break
            else:
                self.items.append(item_entity)
        elif item_entity.item and item_entity.equippable:
            self.equipment.append(item_entity)
        results.append({
            "item_added":
            item_entity,
            "message":
            Message(
                f"You pick up the {item_entity.name}{' (stack of ' + str(item_entity.item.quantity) + ')' if item_entity.item.quantity > 1 else ''}.",
                "light blue")
        })
        return results

    def use(self, item_entity, **kwargs):
        results = []
        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({"equip": item_entity})
            else:
                results.append({
                    "message":
                    Message(f"You can't use the {item_entity.name}.", "yellow")
                })
        else:
            if item_component.targeting and not (kwargs.get("target_x")
                                                 or kwargs.get("target_y")):
                results.append({"targeting": item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(
                    self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get("consumed"):
                        if item_entity.item.quantity >= 2:
                            item_entity.item.quantity -= 1
                        else:
                            self.remove_item(item_entity)

                results.extend(item_use_results)
        return results

    def remove_item(self, item_entity):
        if item_entity.item and not item_entity.equippable:
            self.items.remove(item_entity)
        elif item_entity.item and item_entity.equippable:
            self.equipment.remove(item_entity)

    def drop_item(self, item):
        results = []

        for slot, equipment in self.owner.equipment.__dict__.items():
            if item == equipment:
                self.owner.equipment.toggle_equip(item)
                break

        item.x = self.owner.x
        item.y = self.owner.y

        if item.item.quantity >= 2:
            item.item.quantity -= 1
            results.append({
                "item_quantity_dropped":
                item,
                "message":
                Message(f"You dropped one {item.name}", "yellow")
            })
        else:
            self.remove_item(item)
            results.append({
                "item_dropped":
                item,
                "message":
                Message(f"You dropped the {item.name}", "yellow")
            })
        return results
