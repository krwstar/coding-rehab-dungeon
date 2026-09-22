import time
import random

BASIC = "basic"
COMMON = "common"
RARE = "rare"
EPIC = "epic"
LEGENDARY = "legendary"

def add_battle_log(battle_logs, text):
    battle_logs.append(text)


class Character:
    def __init__(
        self,
        name="",
        max_hp=0,
        max_mp=0,
        speed=0,
        attack=0,
        magic=0,
        defense=0,
        crit_chance=0.05,
        block=0,
        statuses=None,
        skills=None,
        items=None,
        gold=0,
    ):
        self.name = name
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.hp = max_hp
        self.mp = max_mp
        self.speed = speed
        self.attack = attack
        self.magic = magic
        self.defense = defense
        self.crit_chance = crit_chance
        self.block = block
        self.statuses = [] if statuses is None else statuses
        self.skills = [] if skills is None else skills
        self.items = [] if items is None else items
        self.gold = gold
        self.action_gauge = 0
        self.weapon = None
        self.armor = None
        self.ring = None
    
    def get_passives(self):
        passives = []

        for equipment in [self.weapon, self.armor, self.ring]:
            if equipment is None or equipment.passive is None:
                continue
            
            if isinstance(equipment.passive, list):
                passives.extend(equipment.passive)
            else:
                passives.append(equipment.passive)

        return passives
    
    def trigger_battle_start_passive(self, battle_logs):
        for passive in self.get_passives():
            passive.on_battle_start(self, battle_logs)
    
    def trigger_turn_start_passive(self, battle_logs):
        for passive in self.get_passives():
            passive.on_turn_start(self, battle_logs)
                
    def trigger_turn_end_passive(self, battle_logs):
        for passive in self.get_passives():
            passive.on_turn_end(self, battle_logs)
            
    def trigger_deal_damage_statuses(self, target, battle_logs):
        for status in self.statuses[:]:
            status.on_deal_damage(self, target, battle_logs)
        self.cleanup_statuses()
                
    def trigger_deal_damage_passive(self, target, battle_logs):
        for passive in self.get_passives():
            passive.on_deal_damage(self, target, battle_logs)
    
    def trigger_before_take_damage_passives(self, attacker, damage, battle_logs,):
        for passive in self.get_passives():
            damage = passive.on_before_take_damage(self, attacker, damage, battle_logs,)
        return damage
    
    def trigger_take_damage_passive(self, attacker, battle_logs):
        for passive in self.get_passives():
            passive.on_take_damage(self, attacker, battle_logs)
    
    def trigger_hp_damage_passive(self, attacker, hp_damage, battle_logs):
        for passive in self.get_passives():
            passive.on_hp_damage(self, attacker, hp_damage, battle_logs,)
    
    def trigger_skill_use_passive(self, target, battle_logs):
        for passive in self.get_passives():
            passive.on_skill_use(self, target, battle_logs)
    
    def trigger_turn_start_statuses(self, battle_logs):
        can_act = True

        for status in self.statuses[:]:
            result = status.on_turn_start(self, battle_logs)
            if result is False:
                can_act = False

        self.cleanup_statuses()
        return can_act

    def trigger_turn_end_statuses(self, battle_logs):
        for status in self.statuses[:]:
            status.on_turn_end(self, battle_logs)
        self.cleanup_statuses()

    def trigger_before_take_damage_statuses(self, attacker, damage, battle_logs):
        for status in self.statuses[:]:
            damage = status.on_before_take_damage(
                self, attacker, damage, battle_logs
            )
        self.cleanup_statuses()
        return damage

    def trigger_take_damage_statuses(self, attacker, battle_logs):
        for status in self.statuses[:]:
            status.on_take_damage(self, attacker, battle_logs)
    
    def trigger_parry_success_passive(self, attacker, battle_logs):
        for passive in self.get_passives():
            passive.on_parry_success(self, attacker, battle_logs)
            
    def reset_block(self):
        block = 0
        for passive in self.get_passives():
            kept_block = passive.keep_block(self, self.block)
            block = max(block, kept_block)
        self.block = block
    
    def cleanup_statuses(self):
        self.statuses = [
            s for s in self.statuses if not s.is_expired()
        ]


class Equipment:
    def __init__(
        self,
        name,
        slot,
        hp=0,
        mp=0,
        speed=0,
        attack=0,
        magic=0,
        defense=0,
        critical=0,
        damage_dealt_multiplier=0,
        damage_taken_multiplier=0,
        passive=None,
        price=0,
        rarity="basic",
        flavor_text="",
    ):
        self.name = name
        self.slot = slot
        self.hp = hp
        self.mp = mp
        self.speed = speed
        self.attack = attack
        self.magic = magic
        self.defense = defense
        self.critical = critical
        self.damage_dealt_multiplier = damage_dealt_multiplier
        self.damage_taken_multiplier = damage_taken_multiplier
        self.passive = passive
        self.price = price
        self.rarity = rarity
        self.flavor_text = flavor_text


class Weapon(Equipment):
    def __init__(
        self,
        name,
        basic_attack,
        hp=0,
        mp=0,
        speed=0,
        attack=0,
        magic=0,
        defense=0,
        critical=0,
        damage_dealt_multiplier=0,
        damage_taken_multiplier=0,
        passive=None,
        price=0,
        rarity="basic",
        flavor_text="",
    ):
        super().__init__(
            name=name,
            slot="weapon",
            hp=hp,
            mp=mp,
            speed=speed,
            attack=attack,
            magic=magic,
            defense=defense,
            critical=critical,
            damage_dealt_multiplier=damage_dealt_multiplier,
            damage_taken_multiplier=damage_taken_multiplier,
            passive=passive,
            price=price,
            rarity=rarity,
            flavor_text=flavor_text,
        )
        self.basic_attack = basic_attack


class Armor(Equipment):
    def __init__(
        self,
        name,
        defense_action,
        hp=0,
        mp=0,
        speed=0,
        attack=0,
        magic=0,
        defense=0,
        critical=0,
        damage_dealt_multiplier=0,
        damage_taken_multiplier=0,
        passive=None,
        price=0,
        rarity="basic",
        flavor_text="",
    ):
        super().__init__(
            name=name,
            slot="armor",
            hp=hp,
            mp=mp,
            speed=speed,
            attack=attack,
            magic=magic,
            defense=defense,
            critical=critical,
            damage_dealt_multiplier=damage_dealt_multiplier,
            damage_taken_multiplier=damage_taken_multiplier,
            passive=passive,
            price=price,
            rarity=rarity,
            flavor_text=flavor_text,
        )
        self.defense_action = defense_action


class Ring(Equipment):
    def __init__(
        self,
        name,
        hp=0,
        mp=0,
        speed=0,
        attack=0,
        magic=0,
        defense=0,
        critical=0,
        damage_dealt_multiplier=0,
        damage_taken_multiplier=0,
        passive=None,
        price=0,
        rarity="basic",
        flavor_text="",
    ):
        super().__init__(
            name=name,
            slot="ring",
            hp=hp,
            mp=mp,
            speed=speed,
            attack=attack,
            magic=magic,
            defense=defense,
            critical=critical,
            damage_dealt_multiplier=damage_dealt_multiplier,
            damage_taken_multiplier=damage_taken_multiplier,
            passive=passive,
            price=price,
            rarity=rarity,
            flavor_text=flavor_text,
        )


class Item:
    def __init__(
        self,
        name,
        effects=None,
        target_type="self",
        usable_in_battle=True,
        usable_outside_battle=True,
        price=0,
        flavor_text="",
    ):
        self.name = name
        self.effects = [] if effects is None else effects
        self.target_type = target_type
        self.usable_in_battle = usable_in_battle
        self.usable_outside_battle = usable_outside_battle
        self.price = price
        self.flavor_text = flavor_text


class Passive:
    def __init__(
        self,
        name="",
        effects=None,
        attack_bonus=0,
        magic_bonus=0,
        speed_bonus=0,
        defense_bonus=0,
        hp_threshold=None,
    ):
        self.name = name
        self.effects = [] if effects is None else effects
        self.attack_bonus = attack_bonus
        self.magic_bonus = magic_bonus
        self.speed_bonus = speed_bonus
        self.defense_bonus = defense_bonus
        self.hp_threshold = hp_threshold
        
        
    def is_active(self, user):
        if self.hp_threshold is None:
            return True
        return (user.hp / calculate_max_hp(user)) <= self.hp_threshold

    def modify_attack(self, user, attack):
        if self.is_active(user) and self.attack_bonus != 0:
            attack += max(1, int(attack * self.attack_bonus))
        return attack

    def modify_magic(self, user, magic):
        if self.is_active(user) and self.magic_bonus != 0:
            magic += max(1, int(magic * self.magic_bonus))
        return magic

    def on_battle_start(self, user, battle_logs):
        pass
    
    def on_turn_start(self, user, battle_logs):
        pass
    
    def on_turn_end(self, user, battle_logs):
        pass
    
    def on_deal_damage(self, user, target, battle_logs):
        pass
    
    def on_before_take_damage(self, user, attacker, damage, battle_logs):
        return damage
    
    def on_take_damage(self, user, attacker, battle_logs):
        pass
    
    def on_hp_damage(self, user, attacker, hp_damage, battle_logs):
        pass
    
    def on_skill_use(self, user, target, battle_logs):
        pass
    
    def on_parry_success(self, user, attacker, battle_logs):
        pass
    
    def keep_block(self, user, block):
        return 0

class BattleStartPassive(Passive):
    def on_battle_start(self, user, battle_logs):
        for effect in self.effects:
            if user.hp <= 0:
                break
            effect.apply(user, user, battle_logs)


class TurnStartPassive(Passive):
    def on_turn_start(self, user, battle_logs):
        for effect in self.effects:
            if user.hp <= 0:
                break
            effect.apply(user, user, battle_logs)


class TurnEndPassive(Passive):
    def on_turn_end(self, user, battle_logs):
        for effect in self.effects:
            if user.hp <= 0:
                break
            effect.apply(user, user, battle_logs)


class DealDamagePassive(Passive):
    def on_deal_damage(self, user, target, battle_logs):
        for effect in self.effects:
            if user.hp <= 0:
                break
            if effect.target_type == "self":
                effect_target = user
            else:
                effect_target = target
            effect.apply(user, effect_target, battle_logs)


class SkillUsePassive(Passive):
    def on_skill_use(self, user, target, battle_logs):
        for effect in self.effects:
            if user.hp <= 0:
                break
            if effect.target_type == "self":
                effect_target = user
            else:
                effect_target = target
            effect.apply(user, effect_target, battle_logs)


class KeepBlockPassive(Passive):
    def __init__(self, name="", power=0):
        super().__init__(name=name)
        self.power = power

    def keep_block(self, user, block):
        return int(block * self.power)


class TakeDamagePassive(Passive):
    def on_take_damage(self, user, attacker, battle_logs):
        for effect in self.effects:
            if user.hp <= 0:
                break
            if effect.target_type == "self":
                effect_target = user
            else:
                effect_target = attacker
            effect.apply(user, effect_target, battle_logs)


class HpDamagePassive(Passive):
    def on_hp_damage(self, user, attacker, hp_damage, battle_logs):
        if hp_damage <= 0:
            return

        for effect in self.effects:
            if user.hp <= 0:
                break

            if effect.target_type == "self":
                effect_target = user
            else:
                effect_target = attacker

            effect.apply(user, effect_target, battle_logs)


class ParrySuccessPassive(Passive):
    def on_parry_success(self, user, attacker, battle_logs):
        for effect in self.effects:
            if user.hp <= 0:
                break
            if effect.target_type == "self":
                effect_target = user
            else:
                effect_target = attacker

            effect.apply(user, effect_target, battle_logs)


class Action:
    def __init__(
        self,
        name="",
        effects=None,
        mp_cost=0,
        price=0,
        rarity=BASIC,
        flavor_text="",
        description="",
    ):
        self.name = name
        self.effects = [] if effects is None else effects
        self.mp_cost = mp_cost
        self.price = price
        self.rarity = rarity
        self.flavor_text = flavor_text
        self.description = description


class Effect:
    def __init__(self, target_type="enemy"):
        self.target_type = target_type


class DamageEffect(Effect):
    def __init__(
        self,
        power=1,
        flat=0,
        stat="attack",
        dice_count=0,
        dice_sides=0,
        can_crit=True,
        target_type="enemy",
        can_trigger_passives=True,
    ):
        self.power = power
        self.flat=flat
        self.stat = stat
        self.dice_count = dice_count
        self.dice_sides = dice_sides
        self.can_crit = can_crit
        self.target_type = target_type
        self.can_trigger_passives = can_trigger_passives

    def apply(self, user, target, battle_logs):
        base_damage = int(calculate_stat(user, self.stat) * self.power) + self.flat
        dice_damage = roll_dice(self.dice_count, self.dice_sides)
        damage = base_damage + dice_damage
        
        if self.can_crit and random.random() < calculate_stat(user, "crit_chance"):
            add_battle_log(battle_logs, " !!!!! 회심의 일격 !!!!!")
            damage = int(damage * 1.5)
        
        damage = calculate_damage_dealt(user, damage)
        damage = calculate_damage_taken(target, damage)
        damage = target.trigger_before_take_damage_statuses(
            user, damage, battle_logs
        )
        final_damage = damage
        hp_damage, blocked_damage = take_damage(target, damage)

        if isinstance(user, Player):
            user.run_stats["damage_dealt"] += hp_damage

        if isinstance(target, Player):
            target.run_stats["damage_taken"] += hp_damage
            target.run_stats["damage_blocked"] += blocked_damage
        
        if blocked_damage > 0:
            add_battle_log(
                battle_logs,
                f"{target.name}에게 {final_damage}의 데미지! (방어 {blocked_damage})"
            )
        else:
            add_battle_log(
                battle_logs,
                f"{target.name}에게 {final_damage}의 데미지!"
            )
        
        if self.can_trigger_passives:
            user.trigger_deal_damage_passive(target, battle_logs)
            user.trigger_deal_damage_statuses(target, battle_logs)
        
        target.trigger_take_damage_passive(user, battle_logs)
        target.trigger_take_damage_statuses(user, battle_logs)
        target.trigger_hp_damage_passive(user, hp_damage, battle_logs,)


class RestoreHpEffect(Effect):
    def __init__(self, power=1, flat=0, stat="magic", target_type="self"):
        self.power = power
        self.flat = flat
        self.stat = stat
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        base = calculate_stat(user, self.stat)
        heal = int(base * self.power) + self.flat

        old_hp = target.hp
        target.hp = min(target.hp + heal, calculate_max_hp(target))
        actual_heal = target.hp - old_hp

        if isinstance(user, Player):
            user.run_stats["healing"] += actual_heal

        add_battle_log(
            battle_logs,
            f"{target.name}은(는) HP를 {actual_heal} 회복했다!"
        )


class RestoreMpEffect(Effect):
    def __init__(self, power=0, flat=0, stat="magic", target_type="self"):
        self.power = power
        self.flat = flat
        self.stat = stat
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        base = calculate_stat(user, self.stat)
        amount = int(base * self.power) + self.flat

        old_mp = target.mp
        target.mp = min(
            target.mp + amount,
            calculate_max_mp(target),
        )
        recovered = target.mp - old_mp

        add_battle_log(
            battle_logs,
            f"{target.name}은(는) MP를 {recovered} 회복했다!",
        )


class BlockEffect(Effect):
    def __init__(self, power=1, flat=0, stat="defense", target_type="self"):
        self.power = power
        self.flat = flat
        self.stat = stat
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        base = calculate_stat(user, self.stat)
        block = int(base * self.power) + self.flat
        target.block += block

        if isinstance(user, Player):
            user.run_stats["block_gained"] += block
        
        if self.target_type == "self":
            add_battle_log(battle_logs, f"{user.name}은(는) 방어도를 {block}만큼 올렸다!")
        else:
            add_battle_log(battle_logs, f"{user.name}은(는) {target.name}의 방어도를 {block}만큼 올렸다!")


class ActionGaugeEffect(Effect):
    def __init__(self, power=1, flat=0, stat="speed", target_type="self"):
        self.power = power
        self.flat = flat
        self.stat = stat
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        base = calculate_stat(user, self.stat)
        gauge = int(base * self.power) + self.flat
        target.action_gauge += gauge
        
        if gauge >= 0:
            add_battle_log(
                battle_logs,
                f"{target.name}의 행동 게이지가 {gauge} 증가했다!"
            )
        else:
            add_battle_log(
                battle_logs,
                f"{target.name}의 행동 게이지가 {-gauge} 감소했다!"
            )


class ConsumeHpEffect(Effect):
    def __init__(self, power=0, flat=0, target_type="self"):
        self.power = power
        self.flat = flat
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        amount = min(
            target.hp - 1,
            int(target.hp * self.power) + self.flat
        )
        target.hp -= amount

        add_battle_log(
            battle_logs,
            f"{target.name}의 체력이 {amount} 감소했다!"
        )


class ConsumeMpEffect(Effect):
    def __init__(self, power=0, flat=0, target_type="self"):
        self.power = power
        self.flat = flat
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        amount = min(
            target.mp,
            int(target.mp * self.power) + self.flat
        )
        target.mp -= amount

        add_battle_log(
            battle_logs,
            f"{target.name}의 마력이 {amount} 감소했다!"
        )


class ConsumeBlockEffect(Effect):
    def __init__(self, power=1, flat=0, target_type="self"):
        self.power = power
        self.flat = flat
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        amount = min(
            target.block,
            int(target.block * self.power) + self.flat
        )
        target.block -= amount

        add_battle_log(
            battle_logs,
            f"{target.name}의 방어도가 {amount} 감소했다!"
        )


class DesperateStrikeEffect(Effect):
    def __init__(
        self,
        power=2,
        flat=0,
        stat="attack",
        dice_count=2,
        dice_sides=8,
        hp_cost_power=0.5,
        target_type="enemy"
    ):
        self.power = power
        self.flat = flat
        self.stat = stat
        self.dice_count = dice_count
        self.dice_sides = dice_sides
        self.hp_cost_power = hp_cost_power
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        consumed_hp = min(
            user.hp - 1,
            int(user.hp * self.hp_cost_power)
        )
        user.hp -= consumed_hp
        
        add_battle_log(
            battle_logs,
            f"{user.name}의 체력이 {consumed_hp} 감소했다!"
        )
        
        hp_ratio = consumed_hp / calculate_max_hp(user)
        damage_multiplier = hp_ratio * 5
        
        DamageEffect(
            power=(self.power * damage_multiplier),
            flat=self.flat,
            stat=self.stat,
            dice_count=self.dice_count,
            dice_sides=self.dice_sides,
        ).apply(user, target, battle_logs)


class ManaReleaseEffect(Effect):
    def __init__(
        self,
        power=1.5,
        stat="magic",
        dice_count=2,
        dice_sides=8,
        mp_cost_power=0.5,
        mp_damage_power=3,
        target_type="enemy",
    ):
        self.power = power
        self.stat = stat
        self.dice_count = dice_count
        self.dice_sides = dice_sides
        self.mp_cost_power = mp_cost_power
        self.mp_damage_power = mp_damage_power
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        mp_cost = min(
            user.mp,
            int(user.mp * self.mp_cost_power)
        )
        user.mp -= mp_cost
        bonus_damage = int(mp_cost * self.mp_damage_power)
        
        add_battle_log(
            battle_logs,
            f"{user.name}의 마력이 {mp_cost} 감소했다!"
        )

        DamageEffect(
            power=self.power,
            flat=bonus_damage,
            stat=self.stat,
            dice_count=self.dice_count,
            dice_sides=self.dice_sides,
        ).apply(user, target, battle_logs)


class PoisonBurstEffect(Effect):
    def __init__(self, target_type="enemy"):
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        for status in target.statuses:
            if isinstance(status, PoisonStatus):
                take_penetrate_block_damage(target, status.stack)
                add_battle_log(
                    battle_logs,
                    f"{target.name}의 독이 발작했다! {status.stack}의 데미지!"
                )
                return


class MultiplyPoisonEffect(Effect):
    def __init__(self, power=2, target_type="enemy"):
        self.power = power
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        for status in target.statuses:
            if isinstance(status, PoisonStatus):
                before = status.stack
                status.stack = int(status.stack * self.power)

                add_battle_log(
                    battle_logs,
                    f"{target.name}의 독이 {status.stack-before}스택 증가되었다!",
                )
                return

        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 중독 상태가 아니라 독을 증폭시킬 수 없다!"
        )


class AddStatusEffect(Effect):
    def __init__(
        self,
        status_class,
        status_kwargs,
        target_type="enemy",
    ):
        self.status_class = status_class
        self.status_kwargs = status_kwargs
        self.target_type = target_type

    def apply(self, user, target, battle_logs):
        if any(isinstance(status, InvincibleStatus) for status in target.statuses):
            if getattr(self.status_class, "is_debuff", False):
                return
        for status in target.statuses:
            if type(status) is self.status_class:
                status.source = user
                status.stack_status(
                    battle_logs=battle_logs,
                    target=target,
                    **self.status_kwargs
                )
                return

        new_status = self.status_class(source=user, **self.status_kwargs)
        target.statuses.append(new_status)
        new_status.on_first_apply(target, battle_logs)
        return


class Status:
    def __init__(self, name, source=None):
        self.name = name
        self.source = source
    is_debuff = False

    def on_first_apply(self, target, battle_logs):
        pass

    def on_turn_start(self, target, battle_logs):
        pass

    def on_turn_end(self, target, battle_logs):
        pass
    
    def on_before_take_damage(self, target, attacker, damage, battle_logs):
        return damage
    
    def on_take_damage(self, target, attacker, battle_logs):
        pass
    
    def on_deal_damage(self, user, target, battle_logs):
        pass
    
    def modify_attack(self, target, attack):
        return attack

    def modify_magic(self, target, magic):
        return magic    

    def modify_speed(self, target, speed):
        return speed
    
    def modify_defense(self, target, defense):
        return defense

    def modify_damage_dealt(self, target, damage):
        return damage
    
    def modify_damage_taken(self, target, damage):
        return damage
    
    def stack_status(self, battle_logs):
        raise NotImplementedError
    
    def is_expired(self):
        return False


class PoisonStatus(Status):
    def __init__(self, stack, source=None):
        super().__init__(name="독", source=source)
        self.stack = stack
    is_debuff = True

    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{self.source.name}은(는) {target.name}에게 독을 {self.stack}스택 부여했다!",
        )

    def on_turn_start(self, target, battle_logs):
        damage = take_penetrate_block_damage(target, self.stack)

        if isinstance(self.source, Player):
            self.source.run_stats["damage_dealt"] += damage
            self.source.run_stats["poison_damage"] += damage

        if isinstance(target, Player):
            target.run_stats["damage_taken"] += damage
        
        self.stack -= 1
        
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 독으로 {damage}의 데미지를 입었다!"
        )
        
        if self.stack == 0:
            add_battle_log(
                battle_logs,
                f"{target.name}의 독이 사라졌다!"
            )
    
    def stack_status(self, stack, battle_logs, target=None):
        self.stack += stack
        add_battle_log(
            battle_logs,
            f"{self.source.name}은(는) {target.name}의 독을 {stack}스택 증가시켰다!",
        )
    
    def is_expired(self):
        return self.stack <= 0


class BurnStatus(Status):
    def __init__(self, power, duration, source=None):
        super().__init__(name="화상", source=source)
        self.power = power
        self.duration = duration
    is_debuff = True
    
    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{self.source.name}은(는) {target.name}에게 화상을 부여했다! ({self.power}데미지, {self.duration}턴)",
        )
    
    def on_turn_start(self, target, battle_logs):
        damage = take_penetrate_block_damage(target, self.power)
    
        if isinstance(self.source, Player):
            self.source.run_stats["damage_dealt"] += damage
            self.source.run_stats["burn_damage"] += damage

        if isinstance(target, Player):
            target.run_stats["damage_taken"] += damage

        self.duration -= 1
        
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 화상으로 {damage}의 데미지를 입었다!"
        )
        
        if self.duration == 0:
            add_battle_log(
                battle_logs,
                f"{target.name}의 화상이 사라졌다!"
            )
    
    def stack_status(self, power, duration, battle_logs, target=None):
        self.power += power
        self.duration = max(self.duration, duration)
        add_battle_log(
            battle_logs,
            f"{self.source.name}은(는) {target.name}의 화상을 강화시켰다! ({self.power}데미지, {self.duration}턴)",
        )
    
    def is_expired(self):
        return self.duration <= 0

class BleedStatus(Status):
    def __init__(self, stack, source=None):
        super().__init__(name="출혈", source=source)
        self.stack = stack
    is_debuff = True
    
    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{self.source.name}은(는) {target.name}에게 출혈을 {self.stack}스택 부여했다!",
        )
        self.check_explode(target, battle_logs)
    
    def on_turn_start(self, target, battle_logs):
        damage = max(1, int(target.max_hp * 0.01))
        damage = take_penetrate_block_damage(target, damage)
        
        if isinstance(self.source, Player):
            self.source.run_stats["damage_dealt"] += damage
            self.source.run_stats["bleed_damage"] += damage

        if isinstance(target, Player):
            target.run_stats["damage_taken"] += damage
    
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 출혈에 의해 {damage}의 데미지를 입었다!"
        )
    
    def on_turn_end(self, target, battle_logs):
        self.stack -= 1
        
        if self.stack == 0:
            add_battle_log(
                battle_logs,
                f"{target.name}의 출혈이 사라졌다!",
            )
    
    def stack_status(self, stack, target, battle_logs):
        self.stack += stack
        add_battle_log(
            battle_logs,
            f"{self.source.name}은(는) {target.name}의 출혈을 {stack}스택 증가시켰다!",
        )
        self.check_explode(target, battle_logs)
        
    def check_explode(self, target, battle_logs):
        while self.stack >= 10:
            self.stack -= 10
            damage = take_penetrate_block_damage(target, int(max(1, target.max_hp*0.1)+5))
            
            if isinstance(self.source, Player):
                self.source.run_stats["damage_dealt"] += damage
                self.source.run_stats["bleed_damage"] += damage

            if isinstance(target, Player):
                target.run_stats["damage_taken"] += damage
        
            add_battle_log(
                battle_logs,
                " !!!!! 출혈 !!!!! "
            )
            add_battle_log(
                battle_logs,
                f"{target.name}의 출혈이 폭발했다! {damage}의 데미지!"
            )
    
    def is_expired(self):
        return self.stack <= 0


class ColdStatus(Status):
    def __init__(self, stack, source=None):
        super().__init__(name="냉기", source=source)
        self.stack=stack
    is_debuff = True

    def on_first_apply(self, target, battle_logs):
        if any(
            isinstance(status, (FrozenStatus, FreezeImmunityStatus))
            for status in target.statuses
        ):
            target.statuses.remove(self)
            add_battle_log(
                battle_logs,
                f"{target.name}은(는) 동결 직후라 아직 냉기를 부여할 수 없다!"
            )
            return
        
        add_battle_log(
            battle_logs,
            f"{self.source.name}은(는) {target.name}에게 냉기를 {self.stack}스택 부여했다!",
        )
        self.check_explode(target, battle_logs)

    def modify_speed(self, target, speed):
        return max(1, int(speed * 0.8))

    def on_turn_end(self, target, battle_logs):
        self.stack -= 1
        
        if self.stack == 0:
            add_battle_log(
                battle_logs,
                f"{target.name}의 냉기가 사라졌다!",
            )

    def stack_status(self, stack, target, battle_logs):
        self.stack = min(10, self.stack+stack)
        add_battle_log(
            battle_logs,
            f"{self.source.name}은(는) {target.name}의 냉기를 {stack}스택 증가시켰다!",
        )
        self.check_explode(target, battle_logs)

    def check_explode(self, target, battle_logs):
        if self.stack < 10:
            return
        
        self.stack = 0
        target.statuses.append(FrozenStatus(source=self.source))
        target.statuses.remove(self)
        
        add_battle_log(
            battle_logs,
            f" !!!!! 동결 !!!!! "
        )
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 동결되어 행동불능이 되었다!"
        )

    def is_expired(self):
        return self.stack <= 0


class FrozenStatus(Status):
    def __init__(self, duration=1, source=None):
        super().__init__(name="동결", source=source)
        self.duration = duration

    def on_turn_start(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 동결되어 행동할 수 없다!",
        )
        return False

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1

        if self.duration <= 0:
            target.statuses.append(
                FreezeImmunityStatus(source=self.source)
            )

    def modify_speed(self, target, speed):
        return int(speed * 0.8)

    def stack_status(
        self,
        duration=1,
        target=None,
        battle_logs=None,
    ):
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class FreezeImmunityStatus(Status):
    def __init__(self, source=None):
        super().__init__(name="냉기 면역")
        self.expired = False
    is_debuff = True

    def on_turn_end(self, target, battle_logs):
        self.expired = True

    def is_expired(self):
        return self.expired


class CounterStatus(Status):
    def __init__(self, power=1, flat=0, dice_count=1, dice_sides=6,stat="attack", source=None):
        super().__init__(name="반격", source=source)
        self.power = power
        self.flat = flat
        self.stat = stat
        self.dice_count=dice_count
        self.dice_sides=dice_sides
        self.used = False
    
    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 반격의 기회를 노린다!"
        )
        
    def on_take_damage(self, user, attacker, battle_logs):
        if self.used:
            return
    
        self.used = True

        add_battle_log(
            battle_logs,
            f"{user.name}이(가) 반격했다!"
        )
        DamageEffect(
            power=self.power,
            flat=self.flat,
            stat=self.stat,
            dice_count=self.dice_count,
            dice_sides=self.dice_sides,
        ).apply(
            user,
            attacker,
            battle_logs,
        )
     
    def stack_status(
        self,
        power=1,
        flat=0,
        stat="attack",
        dice_count=0,
        dice_sides=0,
        battle_logs=None,
        target=None,
    ):
        self.power = power
        self.flat = flat
        self.stat = stat
        self.dice_count = dice_count
        self.dice_sides = dice_sides
        self.used = False

    def on_turn_start(self, target, battle_logs):
        self.used = True

    def is_expired(self):
        return self.used


class EntrenchStatus(Status):
    def __init__(self, power=0.5, flat=0, duration=3, source=None):
        super().__init__(name="참호화", source=source)
        self.power = power
        self.flat = flat
        self.duration = duration

    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}이(가) 공격을 받을수록 방어 태세를 굳힌다!"
        )

    def on_take_damage(self, target, attacker, battle_logs):
        BlockEffect(
            power=self.power,
            flat=self.flat,
            stat="defense",
            target_type="self",
        ).apply(
            target,
            target,
            battle_logs,
        )

    def on_turn_start(self, target, battle_logs):
        self.duration -= 1

    def stack_status(
        self,
        power=0.5,
        flat=0,
        duration=3,
        battle_logs=None,
        target=None,
    ):
        self.power = max(self.power, power)
        self.flat = max(self.flat, flat)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class ParryStatus(Status):
    def __init__(self, power=2, flat=0, dice_count=1, dice_sides=6, stat="attack", source=None,):
        super().__init__(name="패링", source=source)
        self.power = power
        self.flat = flat
        self.stat = stat
        self.dice_count = dice_count
        self.dice_sides = dice_sides
        self.used = False

    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 공격을 패링할 준비를 한다!"
        )
    
    def on_turn_start(self, target, battle_logs):
        if self.used:
            target.statuses.remove(self)
            return True
        
        AddStatusEffect(
            status_class=VulnerableStatus,
            status_kwargs={
                "power": 0.5,
                "duration": 2,
            },
            target_type="self",
        ).apply(self.source, target, battle_logs)
        self.used = True
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 패링에 실패해 자세가 무너졌다!"
        )
        return False
        

    def on_before_take_damage(self, target, attacker, damage, battle_logs,):
        if self.used:
            return damage

        self.used = True

        add_battle_log(
            battle_logs,
            f"{target.name}이(가) 공격을 패링하고 반격했다!"
        )
        
        DamageEffect(
            power=self.power,
            flat=self.flat,
            stat=self.stat,
            dice_count=self.dice_count,
            dice_sides=self.dice_sides,
        ).apply(
            target,
            attacker,
            battle_logs,
        )
        
        target.trigger_parry_success_passive(attacker, battle_logs)
        ActionGaugeEffect(power=0, flat=100).apply(target, target, battle_logs)

        return 0
    
    def is_expired(self):
        return self.used


class AbsoluteParryStatus(Status):
    def __init__(self, power=1, flat=0, dice_count=1, dice_sides=6, stat="attack", source=None,):
        super().__init__(name="찰나의 패링", source=source)
        self.power = power
        self.flat = flat
        self.stat = stat
        self.dice_count = dice_count
        self.dice_sides = dice_sides
        self.parried_any = False

    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 공격이 들어오는 찰나의 순간을 포착한다!"
        )
    
    def on_turn_start(self, target, battle_logs):
        target.statuses.remove(self)
        
        if self.parried_any:
            return True
            
        AddStatusEffect(
            status_class=VulnerableStatus,
            status_kwargs={
                "power": 0.5,
                "duration": 2,
            },
            target_type="self",
        ).apply(self.source, target, battle_logs)
        
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 패링에 실패해 자세가 무너졌다!"
        )
        return False
        
    def on_before_take_damage(self, target, attacker, damage, battle_logs,):
        self.parried_any = True

        add_battle_log(
            battle_logs,
            f"{target.name}이(가) 공격을 패링하고 반격했다!"
        )
        
        DamageEffect(
            power=self.power,
            flat=self.flat,
            stat=self.stat,
            dice_count=self.dice_count,
            dice_sides=self.dice_sides,
        ).apply(
            target,
            attacker,
            battle_logs,
        )
        
        target.trigger_parry_success_passive(attacker, battle_logs)

        return 0


class StrengthenStatus(Status):
    def __init__(self, power, duration, source=None):
        super().__init__(name="강화", source=source)
        self.power = power
        self.duration = duration
    
    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 강화되었다! 전 스테이터스 {self.duration}턴 동안 {int(self.power*100)}% 강화!"
        )

    def modify_attack(self, target, attack):
        return int(attack * (1 + self.power))

    def modify_magic(self, target, magic):
        return int(magic * (1 + self.power))

    def modify_speed(self, target, speed):
        return max(1, int(speed * (1 + self.power)))

    def modify_defense(self, target, defense):
        return int(defense * (1 + self.power))

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1

    def stack_status(self, power, duration, battle_logs, target=None):
        self.power = max(self.power, power)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class EnfeebleStatus(Status):
    def __init__(self, power, duration, source=None):
        super().__init__(name="쇠약", source=source)
        self.power = power
        self.duration = duration
    is_debuff = True
    
    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}는 쇠약해졌다! 전 스테이터스가 {self.duration}턴 동안 {int(self.power*100)}% 하락!"
        )

    def modify_attack(self, target, attack):
        return int(attack * (1 - self.power))

    def modify_magic(self, target, magic):
        return int(magic * (1 - self.power))

    def modify_speed(self, target, speed):
        return max(1, int(speed * (1 - self.power)))

    def modify_defense(self, target, defense):
        return int(defense * (1 - self.power))

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1

    def stack_status(self, power, duration, battle_logs, target=None):
        self.power = max(self.power, power)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class VulnerableStatus(Status):
    def __init__(self, power, duration, source=None):
        super().__init__(name="취약", source=source)
        self.power = power
        self.duration = duration
    is_debuff = True

    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) {self.duration}턴 동안 취약해졌다! 받는 데미지 {int(self.power*100)}% 증가!"
        )

    def modify_damage_taken(self, target, damage):
        return int(damage * (1 + self.power))

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1

    def stack_status(self, power, duration, battle_logs, target=None):
        self.power = max(self.power, power)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class WeakenStatus(Status):
    def __init__(self, power, duration, source=None):
        super().__init__(name="약화", source=source)
        self.power = power
        self.duration = duration
    is_debuff = True

    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 약화되었다! {self.duration}턴 동안 가하는 데미지 {int(self.power*100)}% 감소!"
        )

    def modify_damage_dealt(self, target, damage):
        return max(0, int(damage * (1 - self.power)))

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1

    def stack_status(self, power, duration, battle_logs, target=None):
        self.power = max(self.power, power)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class FortifyStatus(Status):
    def __init__(self, power, flat, stat, duration, source=None):
        super().__init__(name="요새화", source=source)
        self.power = power
        self.flat = flat
        self.stat = stat
        self.duration = duration
    
    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) {self.duration}턴 동안 턴 시작시 방어도를 획득한다!"
        )

    def on_turn_start(self, target, battle_logs):
        BlockEffect(
            power=self.power,
            flat=self.flat,
            stat=self.stat,
        ).apply(target, target, battle_logs)

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1

    def stack_status(self, power, flat, duration, battle_logs, stat=None, target=None):
        self.power = max(self.power, power)
        self.flat = max(self.flat, flat)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class RegenerationStatus(Status):
    def __init__(self, power, flat, duration, source=None):
        super().__init__(name="재생", source=source)
        self.power = power
        self.flat = flat
        self.duration = duration
    
    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) {self.duration}턴 동안 턴 시작시 HP를 회복한다!"
        )

    def on_turn_start(self, target, battle_logs):
        RestoreHpEffect(
            power=self.power,
            flat=self.flat,
        ).apply(target, target, battle_logs)

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1

    def stack_status(self, power, flat, duration, battle_logs, target=None):
        self.power = max(self.power, power)
        self.flat = max(self.flat, flat)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class ManaRegenerationStatus(Status):
    def __init__(self, power, flat, duration, source=None):
        super().__init__(name="마력 재생", source=source)
        self.power = power
        self.flat = flat
        self.duration = duration
    
    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) {self.duration}턴 동안 턴 시작시 MP를 회복한다!"
        )

    def on_turn_start(self, target, battle_logs):
        RestoreMpEffect(
            power=self.power,
            flat=self.flat,
        ).apply(target, target, battle_logs)

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1

    def stack_status(self, power, flat, duration, battle_logs, target=None):
        self.power = max(self.power, power)
        self.flat = max(self.flat, flat)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0

class HasteStatus(Status):
    def __init__(self, power, flat, duration, source=None):
        super().__init__(name="가속", source=source)
        self.power = power
        self.flat = flat
        self.duration = duration
    
    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) {self.duration}턴 동안 턴 종료시 행동 게이지를 회복한다!"
        )

    def on_turn_end(self, target, battle_logs):
        ActionGaugeEffect(
            power=self.power,
            flat=self.flat,
        ).apply(target, target, battle_logs)
        self.duration -= 1

    def stack_status(self, power, flat, duration, battle_logs, target=None):
        self.power = max(self.power, power)
        self.flat = max(self.flat, flat)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class DodgeStatus(Status):
    def __init__(self, count=1, source=None):
        super().__init__(name="회피", source=source)
        self.count = count

    def on_first_apply(self, target, battle_logs):
        add_battle_log(
            battle_logs,
            f"{target.name}은(는) 다음 공격을 회피할 준비를 한다!"
        )

    def on_turn_start(self, target, battle_logs):
        self.count = 0

    def on_before_take_damage(self, target, attacker, damage, battle_logs,):
        if self.count <= 0:
            return damage

        self.count -= 1

        add_battle_log(
            battle_logs,
            f"{target.name}이(가) 공격을 회피했다!"
        )
        return 0

    def is_expired(self):
        return self.count <= 0
    
    def stack_status(self, count=1, target=None, battle_logs=None,):
        self.count += count


class WorldCooldownStatus(Status):
    def __init__(self, source, duration=11):
        super().__init__(
            name="시간의 부채",
            source=source,
        )
        self.duration = duration
    
    def on_turn_end(self, target, battle_logs):
        self.duration -= 1
    
    def is_expired(self):
        return self.duration <= 0


class ShadowAssaultStatus(Status):
    def __init__(self, power=0.5, duration=3, source=None):
        super().__init__(name="그림자 습격", source=source)
        self.power = power
        self.duration = duration

    def on_deal_damage(self, user, target, battle_logs):
        DamageEffect(
            power=self.power,
            stat="speed",
            can_crit=False,
            can_trigger_passives=False,
        ).apply(user, target, battle_logs)

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1
        
    def stack_status(
    self,
    power=0.5,
    duration=3,
    target=None,
    battle_logs=None,
    ):
        self.power = max(self.power, power)
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class InvincibleStatus(Status):
    def __init__(self, duration, source=None):
        super().__init__(name="무적", source=source)
        self.duration = duration

    def on_before_take_damage(self, target, attacker, damage, battle_logs):
        return 0

    def on_turn_end(self, target, battle_logs):
        self.duration -= 1

    def stack_status(self, duration, target=None, battle_logs=None):
        self.duration = max(self.duration, duration)

    def is_expired(self):
        return self.duration <= 0


class Player(Character):
    def __init__(self, name, skills=None, items=None):
        super().__init__(
            name=name,
            max_hp=30,
            max_mp=20,
            speed=10,
            attack=5,
            magic=5,
            defense=5,
            skills=skills,
            items=items,
            gold=100,
        )

        self.run_stats = {
            "rooms_cleared": 0,
            "battles": 0,
            "wins": 0,
            "damage_dealt": 0,
            "poison_damage": 0,
            "burn_damage": 0,
            "bleed_damage": 0,
            "damage_taken": 0,
            "damage_blocked": 0,
            "healing": 0,
            "block_gained": 0,
            "mp_spent": 0,
            "gold_earned": 0,
            "gold_spent": 0,
            "items_used": {},
            "actions_used": {},
            "room_history": [],
        }

        self.run_start_time = time.time()


class Enemy(Character):
    def __init__(
        self,
        name="",
        max_hp=0,
        max_mp=0,
        speed=0,
        attack=0,
        magic=0,
        defense=0,
        crit_chance=0.05,
        block=0,
        skills=None,
        items=None,
        gold=0,
        action_pool=None,
        action_pools=None,
    ):
        super().__init__(
            name=name,
            max_hp=max_hp,
            max_mp=max_mp,
            speed=speed,
            attack=attack,
            magic=magic,
            defense=defense,
            crit_chance=crit_chance,
            block=block,
            skills=skills,
            items=items,
            gold=gold,
        )
        self.action_pool = action_pool
        self.action_pools = action_pools
        self.action_index = 0


class FinalBoss(Enemy):
    def __init__(
        self,
        name="개발자",
        max_hp=0,
        max_mp=0,
        speed=0,
        attack=0,
        magic=0,
        defense=0,
        crit_chance=0,
        block=0,
        skills=None,
        items=None,
        gold=0,
        action_slots_phase_1=None,
        action_slots_phase_2=None,
        action_slots_phase_3=None,

        cheat_weapon=None,
        cheat_armor=None,
        cheat_ring=None,
    ):
        super().__init__(
            name=name,
            max_hp=max_hp,
            max_mp=max_mp,
            speed=speed,
            attack=attack,
            magic=magic,
            defense=defense,
            crit_chance=crit_chance,
            block=block,
            skills=skills,
            items=items,
            gold=gold,
        )

        self.action_slots_phase_1 = action_slots_phase_1 or []
        self.action_slots_phase_2 = action_slots_phase_2 or []
        self.action_slots_phase_3 = action_slots_phase_3 or []
        
        self.action_index = 0

        self.phase = 1

        self.cheat_weapon = cheat_weapon
        self.cheat_armor = cheat_armor
        self.cheat_ring = cheat_ring
        
        self.developer_action_pending = False

    def select_action(self):
        if self.phase == 1:
            slots = self.action_slots_phase_1
        elif self.phase == 2:
            slots = self.action_slots_phase_2
        elif self.phase == 3:
            slots = self.action_slots_phase_3

        current_index = self.action_index
        slot = slots[current_index]
        self.action_index += 1

        if self.action_index >= len(slots):
            self.action_index = 0

        self.developer_action_pending = (
            self.phase == 3
            and current_index in (2, 5, 8)
        )

        return random.choice(slot)
    
    def check_phase(self, enemy_units, battle_logs):
        if self.hp <= 0:
            return False
        
        if self.phase == 1:
            alive_allies = [
                enemy
                for enemy in enemy_units
                if enemy is not self and enemy.hp > 0
            ]

            if not alive_allies:
                self.enter_phase_2()

                add_battle_log(battle_logs, "")
                add_battle_log(battle_logs, "마지막 사천왕이 쓰러졌다.")
                add_battle_log(battle_logs, "")
                add_battle_log(battle_logs, "개발자는 쓰러진 사천왕들을 잠시 바라보았다.")
                add_battle_log(battle_logs, "")
                add_battle_log(battle_logs, "「...다 잡았네.」")
                add_battle_log(battle_logs, "「생각보다 잘하는데?」")
                add_battle_log(battle_logs, "")
                add_battle_log(battle_logs, "개발자가 천천히 앞으로 걸어 나온다.")
                add_battle_log(battle_logs, "")
                add_battle_log(battle_logs, "「좋아.」")
                add_battle_log(battle_logs, "「이제부터는 내가 상대해 볼까.」")
                add_battle_log(battle_logs, "")
                add_battle_log(battle_logs, "개발자를 감싸는 사천왕의 가호가 사라졌다.")
                add_battle_log(battle_logs, "개발자의 무적 상태가 해제되었다!")
                add_battle_log(battle_logs, "")
                return True

            return False

        if self.phase == 2:
            if self.hp <= 0:
                return False

            if self.hp > calculate_max_hp(self) * 0.5:
                return False

            self.enter_phase_3()

            add_battle_log(battle_logs, "")
            add_battle_log(battle_logs, "개발자가 자신의 상태를 확인했다.")
            add_battle_log(battle_logs, "")
            add_battle_log(battle_logs, "「......벌써 반피인가.」")
            add_battle_log(battle_logs, "")
            add_battle_log(battle_logs, "개발자가 잠시 생각에 잠긴다.")
            add_battle_log(battle_logs, "")
            add_battle_log(battle_logs, "「아-아. 이렇게까지 하고 싶진 않았는데.」")
            add_battle_log(battle_logs, "")
            add_battle_log(battle_logs, "개발자가 인벤토리를 뒤적거리기 시작했다.")
            add_battle_log(battle_logs, "")
            add_battle_log(battle_logs, "「뭐.」")
            add_battle_log(battle_logs, "「있는 걸 안 쓸 이유도 없지.」")
            add_battle_log(battle_logs, "")
            add_battle_log(
                battle_logs,
                f"{self.name}이(가) {self.weapon.name}를 장착했다!"
            )

            add_battle_log(
                battle_logs,
                f"{self.name}이(가) {self.armor.name}를 장착했다!"
            )

            add_battle_log(
                battle_logs,
                f"{self.name}이(가) {self.ring.name}를 장착했다!"
            )
            add_battle_log(battle_logs, "")
            add_battle_log(battle_logs, "개발자가 다시 자세를 잡았다.")
            add_battle_log(battle_logs, "")
            add_battle_log(battle_logs, "「계속하지.」")
            add_battle_log(battle_logs, "")
            return True
        return False

    def enter_phase_2(self):
        self.phase = 2
        self.action_index = 0

        self.statuses = [
            status
            for status in self.statuses
            if not isinstance(status, InvincibleStatus)
        ]

    def enter_phase_3(self):
        self.phase = 3

        self.weapon = self.cheat_weapon
        self.armor = self.cheat_armor
        self.ring = self.cheat_ring
    
    
    def developer_clear_statuses(self, characters, battle_logs):
        add_battle_log(
            battle_logs,
            "「상태가 너무 지저분한데.」"
        )
        add_battle_log(
            battle_logs,
            "[DEV CONSOLE]"
        )
        add_battle_log(
            battle_logs,
            ">>> character.statuses.clear()"
        )

        for character in characters:
            character.statuses.clear()

        add_battle_log(
            battle_logs,
            "... applied to 2 charactes."
        )
        add_battle_log(
            battle_logs,
            "모든 캐릭터에게 적용된 상태 효과가 흔적도 없이 사라졌다!"
        )


    def developer_heal_all(self, characters, battle_logs):
        add_battle_log(
            battle_logs,
            "「너무 빨리 끝나면 재미없잖아?」"
        )
        add_battle_log(
            battle_logs,
            "[DEV CONSOLE]"
        )
        add_battle_log(
            battle_logs,
            ">>> character.hp += 20"
        )
        
        for character in characters:
            character.hp = min(
                character.hp + 20,
                calculate_max_hp(character),
            )
            
        add_battle_log(
            battle_logs,
            "... applied to 2 charactes."
        )
        add_battle_log(
            battle_logs,
            "모든 캐릭터의 HP가 20 회복되었다!"
        )


    def developer_turn_based_mode(self, characters, battle_logs):
        add_battle_log(
            battle_logs,
            "「자꾸 턴 순서가 꼬이네.」"
        )
        add_battle_log(
            battle_logs,
            "「잠깐 턴제로 해볼까?」"
        )
        add_battle_log(
            battle_logs,
            "[DEV CONSOLE]"
        )
        add_battle_log(
            battle_logs,
            ">>> character.action_gauge += 600"
        )

        for character in characters:
            character.action_gauge += 600

        add_battle_log(
            battle_logs,
            "... applied to 2 charactes."
        )
        add_battle_log(
            battle_logs,
            "모든 캐릭터의 행동 게이지가 600 증가했다!"
        )


    def developer_reset_block(self, characters, battle_logs):
        add_battle_log(
            battle_logs,
            "「방어도 너무 많이 쌓인 거 아니야?」"
        )
        add_battle_log(
            battle_logs,
            "[DEV CONSOLE]"
        )
        add_battle_log(
            battle_logs,
            ">>> character.block = 0"
        )

        for character in characters:
            character.block = 0

        add_battle_log(
            battle_logs,
            "... applied to 2 charactes."
        )
        add_battle_log(
            battle_logs,
            "모든 캐릭터의 방어도가 0이 되었다!"
        )
    
    def execute_developer_action(
        self,
        player,
        enemy_units,
        battle_logs,
    ):
        if not self.developer_action_pending:
            return False
        self.developer_action_pending = False        
        
        characters = [
            character
            for character in [player] + enemy_units
            if character.hp > 0
        ]

        actions = [
            self.developer_clear_statuses,
            self.developer_heal_all,
            self.developer_turn_based_mode,
            self.developer_reset_block,
        ]

        action = random.choice(actions)

        add_battle_log(battle_logs, "")
        add_battle_log(
            battle_logs,
            "개발자가 전투 도중 갑자기 허공에 손을 뻗어 콘솔 화면을 띄웠다."
        )
        action(characters, battle_logs)
        add_battle_log(battle_logs, "")
        
        return True


def calculate_stat(user, stat):
    if stat == "attack":
        return calculate_attack_power(user)
    elif stat == "magic":
        return calculate_magic_power(user)
    elif stat == "speed":
        return calculate_speed(user)
    elif stat == "defense":
        return calculate_defense(user)
    elif stat == "crit_chance":
        return calculate_crit_chance(user)
    elif stat == "block":
        return user.block
    else:
        raise ValueError(f"알 수 없는 스탯: {stat}")


def calculate_max_hp(character):
    max_hp = character.max_hp
    if character.weapon is not None:
        max_hp += character.weapon.hp
    if character.armor is not None:
        max_hp += character.armor.hp
    if character.ring is not None:
        max_hp += character.ring.hp
    return max_hp


def calculate_max_mp(character):
    max_mp = character.max_mp
    if character.weapon is not None:
        max_mp += character.weapon.mp
    if character.armor is not None:
        max_mp += character.armor.mp
    if character.ring is not None:
        max_mp += character.ring.mp
    return max_mp


def calculate_attack_power(character):
    attack = character.attack
    if character.weapon is not None:
        attack += character.weapon.attack
    if character.armor is not None:
        attack += character.armor.attack
    if character.ring is not None:
        attack += character.ring.attack
    for passive in character.get_passives():
        attack = passive.modify_attack(character, attack)
    for status in character.statuses:
        attack = status.modify_attack(character, attack)
    return attack


def calculate_magic_power(character):
    magic = character.magic
    if character.weapon is not None:
        magic += character.weapon.magic
    if character.armor is not None:
        magic += character.armor.magic
    if character.ring is not None:
        magic += character.ring.magic
    for status in character.statuses:
        magic = status.modify_magic(character, magic)
    for passive in character.get_passives():
        magic = passive.modify_magic(character, magic)
    return magic



def calculate_speed(character):
    speed = character.speed
    if character.weapon is not None:
        speed += character.weapon.speed
    if character.armor is not None:
        speed += character.armor.speed
    if character.ring is not None:
        speed += character.ring.speed
    
    for status in character.statuses:
        speed = status.modify_speed(character, speed)
    
    return speed


def calculate_defense(character):
    defense = character.defense
    if character.weapon is not None:
        defense += character.weapon.defense
    if character.armor is not None:
        defense += character.armor.defense
    if character.ring is not None:
        defense += character.ring.defense
    
    for status in character.statuses:
        defense = status.modify_defense(character, defense)
    
    return defense


def calculate_crit_chance(character):
    crit_chance = character.crit_chance
    if character.weapon is not None:
        crit_chance += character.weapon.critical
    if character.armor is not None:
        crit_chance += character.armor.critical
    if character.ring is not None:
        crit_chance += character.ring.critical
    return crit_chance


def calculate_damage_dealt(character, damage):
    damage_dealt_multiplier = 0

    if character.weapon is not None:
        damage_dealt_multiplier += character.weapon.damage_dealt_multiplier
    if character.armor is not None:
        damage_dealt_multiplier += character.armor.damage_dealt_multiplier
    if character.ring is not None:
        damage_dealt_multiplier += character.ring.damage_dealt_multiplier

    damage = int(damage * (1 + damage_dealt_multiplier))

    for status in character.statuses:
        damage = status.modify_damage_dealt(character, damage)

    return damage


def calculate_damage_taken(character, damage):
    damage_taken_multiplier = 0
    
    if character.weapon is not None:
        damage_taken_multiplier += character.weapon.damage_taken_multiplier
    if character.armor is not None:
        damage_taken_multiplier += character.armor.damage_taken_multiplier
    if character.ring is not None:
        damage_taken_multiplier += character.ring.damage_taken_multiplier
    
    damage = int(damage * (1 + damage_taken_multiplier))
    
    for status in character.statuses:
        damage = status.modify_damage_taken(character, damage)
    
    return damage


def roll_dice(count, sides):
    value = 0
    for _ in range(count):
        value += random.randint(1, sides)
    return value


def take_damage(target, damage):
    blocked_damage = min(target.block, damage)
    damage_after_block = damage - blocked_damage

    target.block -= blocked_damage

    old_hp = target.hp
    target.hp = max(target.hp - damage_after_block, 0)
    actual_hp_damage = old_hp - target.hp

    return actual_hp_damage, blocked_damage


def take_penetrate_block_damage(target, damage):
    old_hp = target.hp
    target.hp = max(0, target.hp - damage)
    return old_hp - target.hp
