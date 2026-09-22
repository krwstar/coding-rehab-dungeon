from models import (
    Weapon,
    Armor,
    Ring,
    Item,
    Enemy,
    FinalBoss,
    Action,
    
    Passive,
    TurnStartPassive,
    TurnEndPassive,
    BattleStartPassive,
    SkillUsePassive,
    DealDamagePassive,
    KeepBlockPassive,
    TakeDamagePassive,
    ParrySuccessPassive,
    HpDamagePassive,
    
    Effect,
    DamageEffect,
    RestoreHpEffect,
    RestoreMpEffect,
    BlockEffect,
    ActionGaugeEffect,
    AddStatusEffect,
    ConsumeBlockEffect,
    DesperateStrikeEffect,
    ManaReleaseEffect,
    PoisonBurstEffect,
    MultiplyPoisonEffect,
    
    Status,
    PoisonStatus,
    BurnStatus,
    BleedStatus,
    ColdStatus,
    FrozenStatus,
    FreezeImmunityStatus,
    CounterStatus,
    StrengthenStatus,
    EnfeebleStatus,
    VulnerableStatus,
    WeakenStatus,
    FortifyStatus,
    RegenerationStatus,
    ManaRegenerationStatus,
    HasteStatus,
    ParryStatus,
    AbsoluteParryStatus,
    DodgeStatus,
    EntrenchStatus,
    InvincibleStatus,
    WorldCooldownStatus,
    ShadowAssaultStatus,
)

BASIC = "basic"
COMMON = "Common"
RARE = "Rare"
EPIC = "Epic"
LEGENDARY = "Legendary"

items = [
    Item(
        name="하급 체력 포션",
        effects=[
            RestoreHpEffect(
                power=0,
                flat=10,
                target_type="self",
            ),
        ],
        usable_in_battle=True,
        usable_outside_battle=True,
        price=30,
        flavor_text="마시면 HP를 10 회복한다.",
    ),
    Item(
        name="하급 마력 포션",
        effects=[
            RestoreMpEffect(
                power=0,
                flat=10,
                target_type="self",
            ),
        ],
        usable_in_battle=True,
        usable_outside_battle=True,
        price=30,
        flavor_text="마시면 MP를 10 회복한다.",
    ),
    Item(
        name="중급 체력 포션",
        effects=[
            RestoreHpEffect(
                power=0,
                flat=20,
                target_type="self",
            ),
        ],
        usable_in_battle=True,
        usable_outside_battle=True,
        price=60,
        flavor_text="마시면 HP를 20 회복한다.",
    ),
    Item(
        name="중급 마력 포션",
        effects=[
            RestoreMpEffect(
                power=0,
                flat=20,
                target_type="self",
            ),
        ],
        usable_in_battle=True,
        usable_outside_battle=True,
        price=60,
        flavor_text="마시면 MP를 20 회복한다.",
    ),
    Item(
        name="상급 체력 포션",
        effects=[
            RestoreHpEffect(
                power=0,
                flat=30,
                target_type="self",
            ),
        ],
        usable_in_battle=True,
        usable_outside_battle=True,
        price=100,
        flavor_text="마시면 HP를 30 회복한다.",
    ),
    Item(
        name="상급 마력 포션",
        effects=[
            RestoreMpEffect(
                power=0,
                flat=30,
                target_type="self",
            ),
        ],
        usable_in_battle=True,
        usable_outside_battle=True,
        price=100,
        flavor_text="마시면 MP를 30 회복한다.",
    ),
    Item(
        name="고블린 폭탄",
        effects=[
            DamageEffect(power=0, flat=5, dice_count=4, dice_sides=10),
            ActionGaugeEffect(power=0, flat=200),
        ],
        target_type="all_enemies",
        usable_in_battle=True,
        usable_outside_battle=False,
        price=80,
        flavor_text="던지면 모든 적에게 4d10+5의 데미지를 입힌다. 사용 시 턴을 소모하지 않는다.",
    ),
    Item(
        name="화염병",
        effects=[
            DamageEffect(power=0, flat=0, dice_count=3, dice_sides=6),
            AddStatusEffect(status_class=BurnStatus, status_kwargs={"power": 6, "duration": 4}),
            ActionGaugeEffect(power=0, flat=200),
        ],
        target_type="all_enemies",
        usable_in_battle=True,
        usable_outside_battle=False,
        price=80,
        flavor_text="던지면 모든 적에게 3d6의 데미지와 4턴간 6의 화상을 입힌다. 사용 시 턴을 소모하지 않는다.",
    ),
    Item(
        name="에너지 드링크",
        effects=[
            AddStatusEffect(
                status_class=HasteStatus,
                status_kwargs={
                    "power": 0,
                    "flat": 100,
                    "duration": 3
                },
            ),
        ],
        target_type="self",
        usable_in_battle=True,
        usable_outside_battle=False,
        price=70,
        flavor_text="컴공과의 생명수. 마시면 3턴간 턴 종료 시 행동 게이지를 100 회복한다.",
    ),
    Item(
        name="방어 물약",
        effects=[
            BlockEffect(power=0, flat=40),
        ],
        target_type="self",
        usable_in_battle=True,
        usable_outside_battle=False,
        price=65,
        flavor_text="마시면 즉시 방어도를 40 획득한다.",
    ),
    Item(
        name="연막탄",
        effects=[
            AddStatusEffect(
                status_class=WeakenStatus,
                status_kwargs={
                    "power": 0.2,
                    "duration": 3
                },
            ),
            AddStatusEffect(
                status_class=DodgeStatus,
                status_kwargs={
                    "count": 2,
                },
                target_type="self",
            ),
        ],
        target_type="all_enemies",
        usable_in_battle=True,
        usable_outside_battle=False,
        price=70,
        flavor_text="던지면 모든 적을 3턴간 약화시키고 자신에게 회피를 2 부여한다.",
    ),
]

weapons = [
    # 커먼 무기
    Weapon(
        name="철 검",
        attack=3,
        price=50,
        basic_attack=Action(
            name="베기",
            effects=[
                DamageEffect(
                    power=1.2,
                    stat="attack",
                    dice_count=1,
                    dice_sides=6,
                ),
            ],
            flavor_text="철 검을 휘둘렀다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "기본 공격 [베기]: ATK × 1.2 + 1d6\n"
            "적당히 무게감 있는 철 검이다."
        )
    ),
    Weapon(
        name="단검",
        attack=1,
        speed=2,
        critical=0.05,
        price=50,
        basic_attack=Action(
            name="연속 찌르기",
            effects=[
                DamageEffect(
                    power=0.5,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.5,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
            ],
            flavor_text="단검으로 빠르게 두 번 찔렀다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "기본 공격 [연속 찌르기]: SPD × 0.5 + 1d3 (2회)\n"
            "가볍고 다루기 쉬운 단검이다."
        )
    ),
    Weapon(
        name="마법봉",
        magic=3,
        price=50,
        basic_attack=Action(
            name="마력탄",
            effects=[
                DamageEffect(
                    power=0.8,
                    stat="magic",
                    dice_count=1,
                    dice_sides=4,
                ),
            ],
            flavor_text="응축한 마력을 발사했다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "기본 공격 [마력탄]: MAG × 0.8 + 1d4\n"
            "기초적인 마법봉이다."
        )
    ),
    Weapon(
        name="철제 방패",
        defense=5,
        speed=-1,
        price=80,
        basic_attack=Action(
            name="방패치기",
            effects=[
                DamageEffect(
                    power=0.5,
                    stat="defense",
                    dice_count=1,
                    dice_sides=4,
                ),
                AddStatusEffect(
                    status_class=CounterStatus,
                    status_kwargs={
                        "power": 0.7,
                        "stat": "defense",
                        "dice_count": 1,
                        "dice_sides": 4,
                    },
                    target_type="self",
                ),
            ],
            flavor_text="방패로 적을 후려치고 반격할 준비를 했다!",
        ),
        passive=TakeDamagePassive(
            name="반동",
            effects=[
                DamageEffect(
                    power=0.1,
                    stat="defense",
                ),
            ],
        ),
        rarity=COMMON,
        flavor_text=(
            "기본 공격 [방패치기]: DEF × 0.5 + 1d4 / 반격: DEF × 0.7 + 1d4\n"
            "패시브 [반동]: 피격 시 DEF × 0.1 데미지\n"
            "공격을 받아내기 위한 철제 방패. 직접 공격은 약하지만, 공격 후 한 차례 강하게 반격할 수 있다."
        ),
    ),
    Weapon(
        name="대검",
        attack=5,
        speed=-2,
        price=80,
        basic_attack=Action(
            name="대검 휘두르기",
            effects=[
                DamageEffect(
                    power=1.4,
                    stat="attack",
                    dice_count=1,
                    dice_sides=8,
                ),
            ],
            flavor_text="묵직한 대검을 힘껏 휘둘렀다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "기본 공격 [대검 휘두르기]: ATK × 1.4 + 1d8\n"
            "느리지만 강력한 한 방을 가하는 거대한 검이다."
        ),
    ),
    Weapon(
        name="연습용 도",
        attack=2,
        speed=1,
        price=50,
        basic_attack=Action(
            name="참격",
            effects=[
                DamageEffect(
                    power=1.0,
                    stat="attack",
                    dice_count=1,
                    dice_sides=6,
                ),
            ],
            flavor_text="가볍게 적을 베어냈다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "기본 공격 [참격]: ATK × 1.0 + 1d6\n"
            "검술을 익히기 위한 평범한 도. 가볍고 다루기 쉽다."
        ),
    ),
    
    # 레어 무기
    Weapon(
        name="핏빛 대검",
        hp=5,
        attack=5,
        speed=-1,
        price=95,
        basic_attack=Action(
            name="베어 가르기",
            effects=[
                DamageEffect(
                    power=1.3,
                    dice_count=1,
                    dice_sides=6,
                ),
            ],
            flavor_text="핏빛 대검으로 적을 베어 갈랐다!",
        ),
        passive=DealDamagePassive(
            name="피의 갈증",
            effects=[
                AddStatusEffect(
                    status_class=BleedStatus,
                    status_kwargs={"stack": 1},
                ),
                RestoreHpEffect(
                    power=0.1,
                    flat=0,
                    stat="attack",
                    target_type="self",
                ),
            ],
        ),
        rarity=RARE,
        flavor_text=(
            "기본 공격 [베어 가르기]: ATK × 1.3 + 1d6\n"
            "패시브 [피의 갈증]: 공격 적중 시 출혈 1 부여, HP ATK × 0.1 회복\n"
            "피를 머금은 듯 검붉은 대검. 상처를 낼수록 착용자의 기운을 조금씩 되돌려준다."
        ),
    ),
    Weapon(
        name="파쇄의 대검",
        hp=5,
        attack=5,
        speed=-1,
        price=75,
        basic_attack=Action(
            name="파쇄",
            effects=[
                DamageEffect(
                    power=1.5,
                    stat="attack",
                    dice_count=1,
                    dice_sides=8,
                ),
                AddStatusEffect(
                    status_class=VulnerableStatus,
                    status_kwargs={
                        "power": 0.25,
                        "duration": 2,
                    },
                ),
            ],
            flavor_text="무거운 대검을 내리쳐 적의 방어를 무너뜨렸다!",
        ),
        rarity=RARE,
        flavor_text=(
            "기본 공격 [파쇄]: ATK × 1.5 + 1d8 / 취약 25% 부여 (2턴)\n"
            "묵직한 일격에 특화된 대검. 적의 방어를 무너뜨리는 데 효과적이다."
        ),
    ),
    Weapon(
        name="화염의 지팡이",
        mp=3,
        magic=5,
        price=75,
        basic_attack=Action(
            name="화염 파동",
            effects=[
                DamageEffect(
                    power=0.5,
                    stat="magic",
                    dice_count=1,
                    dice_sides=4,
                    target_type="all_enemies",
                ),
            ],
            flavor_text="불꽃의 파동을 일으켜 모든 적을 휩쓸었다!",
        ),
        passive=DealDamagePassive(
            name="발화",
            effects=[
                AddStatusEffect(
                    status_class=BurnStatus,
                    status_kwargs={
                        "power": 1,
                        "duration": 2,
                    },
                ),
            ],
        ),
        rarity=RARE,
        flavor_text=(
            "기본 공격 [화염 파동]: 모든 적에게 MAG × 0.5 + 1d4\n"
            "패시브 [발화]: 공격 적중 시 화상 1 부여 (2턴)\n"
            "화염 속성에 특화된 지팡이. 피해를 줄 때마다 적을 불태운다."
        ),
    ),
    Weapon(
        name="냉기의 지팡이",
        mp=3,
        magic=5,
        price=75,
        basic_attack=Action(
            name="냉기탄",
            effects=[
                DamageEffect(
                    power=0.8,
                    stat="magic",
                    dice_count=1,
                    dice_sides=6,
                ),
                AddStatusEffect(
                    status_class=ColdStatus,
                    status_kwargs={"stack": 1},
                ),
            ],
            flavor_text="냉기를 응축한 탄환을 적에게 발사했다!",
        ),
        passive=DealDamagePassive(
            name="한기",
            effects=[
                AddStatusEffect(
                    status_class=ColdStatus,
                    status_kwargs={
                        "stack": 1,
                    },
                ),
            ],
        ),
        rarity=RARE,
        flavor_text=(
            "기본 공격 [냉기탄]: MAG × 0.8 + 1d6 / 냉기 1 부여\n"
            "패시브 [한기]: 공격 적중 시 냉기 1 부여\n"
            "냉기 속성에 특화된 지팡이. 차가운 마력으로 적을 서서히 얼어붙게 한다."
        ),
    ),
    Weapon(
        name="도적의 쌍단도",
        attack=2,
        speed=3,
        critical=0.07,
        price=85,
        basic_attack=Action(
            name="쌍단도 난무",
            effects=[
                DamageEffect(
                    power=0.45,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.45,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.45,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
            ],
            flavor_text="두 자루의 단도로 적을 빠르게 난도질했다!",
        ),
        passive=DealDamagePassive(
            name="연격의 흐름",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=5,
                    target_type="self",
                ),
            ],
        ),
        rarity=RARE,
        flavor_text=(
            "기본 공격 [쌍단도 난무]: SPD × 0.45 + 1d3 (×3회)\n"
            "패시브 [연격의 흐름]: 공격 적중 시 행동 게이지 +5\n"
            "도적들이 애용하는 한 쌍의 단도. 빠른 연격으로 끊임없이 공격을 이어나간다."
        ),
    ),
    Weapon(
        name="독사의 단검",
        attack=2,
        speed=3,
        critical=0.07,
        price=85,
        basic_attack=Action(
            name="독니",
            effects=[
                DamageEffect(
                    power=0.6,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.6,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
            ],
            flavor_text="독이 밴 두 자루의 단검으로 적을 연달아 찔렀다!",
        ),
        passive=DealDamagePassive(
            name="독성 침투",
            effects=[
                AddStatusEffect(
                    status_class=PoisonStatus,
                    status_kwargs={"stack": 1},
                ),
            ],
        ),
        rarity=RARE,
        flavor_text=(
            "기본 공격 [독니]: SPD × 0.6 + 1d3 (×2회)\n"
            "패시브 [독성 침투]: 공격 적중 시 독 1 부여\n"
            "맹독을 머금은 한 쌍의 단도. 작은 상처조차 치명적인 독으로 이어진다."
        ),
    ),
    Weapon(
        name="돌격 방패",
        defense=7,
        speed=-1,
        price=100,
        basic_attack=Action(
            name="방패 강타",
            effects=[
                DamageEffect(
                    power=0.6,
                    stat="defense",
                    dice_count=1,
                    dice_sides=6,
                ),
                AddStatusEffect(
                    status_class=CounterStatus,
                    status_kwargs={
                        "power": 0.9,
                        "stat": "defense",
                        "dice_count": 1,
                        "dice_sides": 6,
                    },
                    target_type="self",
                ),
            ],
            flavor_text="방패로 적을 강하게 밀어붙이고 반격 태세를 취했다!",
        ),
        passive=TakeDamagePassive(
            name="반동",
            effects=[
                DamageEffect(
                    power=0.15,
                    flat=1,
                    stat="defense",
                ),
            ],
        ),
        rarity=RARE,
        flavor_text=(
            "기본 공격 [방패 강타]: DEF × 0.6 + 1d6 / 반격: DEF × 0.9 + 1d6\n"
            "패시브 [반동]: 피격 시 DEF × 0.1 데미지\n"
            "적의 공격을 정면으로 받아내기 위해 제작된 중형 방패. 공격 후 한 차례 강력한 반격을 준비한다."
        ),
    ),
    Weapon(
        name="중철퇴",
        defense=7,
        speed=-1,
        price=100,
        basic_attack=Action(
            name="중철퇴 강타",
            effects=[
                DamageEffect(
                    power=0.8,
                    stat="block",
                    dice_count=1,
                    dice_sides=6,
                ),
                ConsumeBlockEffect(power=1),
            ],
            flavor_text="축적한 방어를 힘으로 전환해 적을 힘껏 후려쳤다!",
        ),
        rarity=RARE,
        flavor_text=(
            "기본 공격 [중철퇴 강타]: 방어도 × 0.8 + 1d6 / 현재 방어도 전부 소모\n"
            "축적한 방어도를 파괴적인 일격으로 전환하는 거대한 철퇴."
        ),
    ),
    Weapon(
        name="무명도",
        attack=4,
        speed=3,
        basic_attack=Action(
            name="일섬",
            effects=[
                DamageEffect(
                    power=1.0,
                    stat="attack",
                    dice_count=1,
                    dice_sides=6,
                ),
            ],
            flavor_text="번뜩이는 칼날로 적을 베어냈다!",
        ),
        passive=ParrySuccessPassive(
            name="응수",
            effects=[
                DamageEffect(
                    power=0.5,
                    stat="attack",
                    dice_count=1,
                    dice_sides=4,
                ),
            ],
        ),
        price=100,
        rarity=RARE,
        flavor_text=(
            "기본 공격 [일섬]: ATK × 1.0 + 1d6\n"
            "패시브 [응수]: 패링 성공 시 ATK × 0.5 + 1d4 추가타\n"
            "이름 없는 장인이 벼린 듯한 도. 공격을 흘려낸 순간, 빈틈을 놓치지 않고 칼끝이 뒤따른다."
        ),
    ),

    # 에픽 무기
    Weapon(
        name="선혈의 대검",
        hp=10,
        attack=7,
        speed=-2,
        price=140,
        basic_attack=Action(
            name="피의 참격",
            effects=[
                DamageEffect(
                    power=1.4,
                    stat="attack",
                    dice_count=1,
                    dice_sides=8,
                ),
            ],
            flavor_text="선혈을 머금은 대검으로 적을 거칠게 베어냈다!",
        ),
        passive=DealDamagePassive(
            name="피의 향연",
            effects=[
                AddStatusEffect(
                    status_class=BleedStatus,
                    status_kwargs={
                        "stack": 2,
                    },
                ),
                RestoreHpEffect(
                    power=0.2,
                    stat="attack",
                )
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "기본 공격 [피의 참격]: ATK × 1.4 + 1d8\n"
            "패시브 [피의 향연]: 공격 적중 시 출혈 2 부여 / ATK의 20%만큼 HP 회복\n"
            "피를 머금을수록 더욱 흉포해지는 거대한 대검."
        ),
    ),
    Weapon(
        name="분쇄의 대검",
        hp=10,
        attack=7,
        speed=-2,
        price=140,
        basic_attack=Action(
            name="분쇄",
            effects=[
                DamageEffect(
                    power=2.0,
                    stat="attack",
                    dice_count=1,
                    dice_sides=10,
                ),
                AddStatusEffect(
                    status_class=VulnerableStatus,
                    status_kwargs={
                        "power": 0.25,
                        "duration": 3,
                    },
                ),
            ],
            flavor_text="대검을 힘껏 내리쳐 적의 자세를 완전히 무너뜨렸다!",
        ),
        rarity=EPIC,
        flavor_text=(
            "기본 공격 [분쇄]: ATK × 2.0 + 1d10 / 취약 25% 부여 (3턴)\n"
            "압도적인 무게로 적을 분쇄하는 대검."
        ),
    ),
    Weapon(
        name="겁화의 지팡이",
        mp=10,
        magic=7,
        price=140,
        basic_attack=Action(
            name="화염탄 연사",
            effects=[
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                    target_type="all_enemies",
                ),
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                    target_type="all_enemies",
                ),
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                    target_type="all_enemies",
                ),
            ],
            flavor_text="화염탄을 연달아 쏘아 모든 적을 불태웠다!",
        ),
        passive=DealDamagePassive(
            name="작열",
            effects=[
                AddStatusEffect(
                    status_class=BurnStatus,
                    status_kwargs={
                        "power": 2,
                        "duration": 2,
                    },
                ),
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "기본 공격 [화염탄 연사]: 모든 적에게 MAG × 0.3 + 1d3 (×3회)\n"
            "패시브 [작열]: 공격 적중 시 화상 2 부여 (2턴)\n"
            "격렬한 불길을 머금은 지팡이. 쏟아지는 화염탄이 전장을 불길로 뒤덮는다."
        ),
    ),
    Weapon(
        name="빙하의 지팡이",
        mp=10,
        magic=7,
        price=140,
        basic_attack=Action(
            name="빙창 연사",
            effects=[
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                ),
            ],
            flavor_text="얼음의 창을 연달아 쏘아 적을 꿰뚫었다!",
        ),
        passive=DealDamagePassive(
            name="혹한",
            effects=[
                AddStatusEffect(
                    status_class=ColdStatus,
                    status_kwargs={
                        "stack": 2,
                    },
                ),
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "기본 공격 [빙창 연사]: MAG × 0.3 + 1d3 (×3회)\n"
            "패시브 [혹한]: 공격 적중 시 냉기 2 부여\n"
            "극한의 냉기를 품은 지팡이. 연이어 쏘아낸 빙창이 적을 얼어붙게 한다."
        ),
    ),
    Weapon(
        name="잔영의 쌍단도",
        attack=3,
        speed=5,
        critical=0.1,
        price=140,
        basic_attack=Action(
            name="잔영 난무",
            effects=[
                DamageEffect(
                    power=0.4,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.4,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.4,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.4,
                    stat="speed",
                    dice_count=1,
                    dice_sides=3,
                ),
            ],
            flavor_text="잔영을 남기며 적을 순식간에 난도질했다!",
        ),
        passive=DealDamagePassive(
            name="잔영의 흐름",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=6,
                    target_type="self",
                ),
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "기본 공격 [잔영 난무]: SPD × 0.4 + 1d3 (×4회)\n"
            "패시브 [잔영의 흐름]: 공격 적중 시 행동 게이지 +6\n"
            "눈으로 쫓기 어려울 만큼 빠른 연격을 가능하게 하는 한 쌍의 단도."
        ),
    ),
    Weapon(
        name="맹독의 단검",
        attack=2,
        speed=4,
        critical=0.1,
        price=140,
        basic_attack=Action(
            name="맹독의 연격",
            effects=[
                DamageEffect(
                    power=0.7,
                    stat="speed",
                    dice_count=1,
                    dice_sides=4,
                ),
                DamageEffect(
                    power=0.7,
                    stat="speed",
                    dice_count=1,
                    dice_sides=4,
                ),
            ],
            flavor_text="맹독이 밴 두 자루의 단검으로 적을 연달아 찔렀다!",
        ),
        passive=DealDamagePassive(
            name="맹독",
            effects=[
                AddStatusEffect(
                    status_class=PoisonStatus,
                    status_kwargs={"stack": 2},
                ),
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "기본 공격 [맹독의 연격]: SPD × 0.7 + 1d4 (×2회)\n"
            "패시브 [맹독]: 공격 적중 시 독 2 부여\n"
            "치명적인 맹독이 스며든 한 쌍의 단도."
        ),
    ),
    Weapon(
        name="가시 대방패",
        defense=9,
        hp=5,
        speed=-2,
        price=140,
        basic_attack=Action(
            name="방패 돌진",
            effects=[
                DamageEffect(
                    power=0.7,
                    stat="defense",
                    dice_count=1,
                    dice_sides=8,
                ),
                AddStatusEffect(
                    status_class=CounterStatus,
                    status_kwargs={
                        "power": 1.1,
                        "stat": "defense",
                        "dice_count": 1,
                        "dice_sides": 8,
                    },
                    target_type="self",
                ),
            ],
            flavor_text="대방패를 앞세워 적을 거세게 밀어붙이고 반격 태세를 취했다!",
        ),
        passive=TakeDamagePassive(
            name="가시",
            effects=[
                DamageEffect(
                    power=0.25,
                    stat="defense",
                    dice_count=1,
                    dice_sides=2,
                ),
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "기본 공격 [방패 돌진]: DEF × 0.7 + 1d8 / 반격: DEF × 1.1 + 1d8\n"
            "패시브 [가시]: 피격 시 DEF × 0.25 + 1d2 데미지\n"
            "날카로운 가시가 돋아난 거대한 방패. 공격을 받아내는 것만으로도 상대에게 상처를 남긴다."
        ),
    ),
    Weapon(
        name="공성 철퇴",
        defense=9,
        hp=5,
        speed=-2,
        price=140,
        basic_attack=Action(
            name="공성 강타",
            effects=[
                DamageEffect(
                    power=1.0,
                    stat="block",
                    dice_count=1,
                    dice_sides=8,
                ),
                ConsumeBlockEffect(power=1),
            ],
            flavor_text="축적한 방어를 모두 실어 적을 짓뭉갰다!",
        ),
        rarity=EPIC,
        flavor_text=(
            "기본 공격 [공성 강타]: 방어도 × 1.0 + 1d8 / 현재 방어도 전부 소모\n"
            "성문을 무너뜨리기 위해 만들어진 거대한 철퇴."
        ),
    ),
    Weapon(
        name="명도 히나타츠카미",
        attack=6,
        speed=4,
        basic_attack=Action(
            name="섬화",
            effects=[
                DamageEffect(
                    power=1.1,
                    stat="attack",
                    dice_count=1,
                    dice_sides=8,
                ),
            ],
            flavor_text="섬광처럼 번뜩이는 칼날로 적을 베어냈다!",
        ),
        passive=ParrySuccessPassive(
            name="역섬",
            effects=[
                DamageEffect(
                    power=0.8,
                    stat="attack",
                    dice_count=1,
                    dice_sides=6,
                ),
            ],
        ),
        price=140,
        rarity=EPIC,
        flavor_text=(
            "기본 공격 [섬화]: ATK × 1.1 + 1d8\n"
            "패시브 [역섬]: 패링 성공 시 ATK × 0.8 + 1d6 추가타\n"
            "이름난 장인이 벼린 명도. 공격을 흘려낸 찰나, 더욱 날카로운 칼끝이 뒤따른다."
        ),
    ),
    
    # 레전더리 무기
    Weapon(
        name="피에 굶주린 대검",
        hp=15,
        attack=10,
        speed=-3,
        price=200,
        basic_attack=Action(
            name="피에 굶주린 일격",
            effects=[
                DamageEffect(
                    power=1.5,
                    stat="attack",
                    dice_count=1,
                    dice_sides=10,
                )
            ],
            flavor_text="피에 굶주린 대검으로 적을 거칠게 베어냈다!",
        ),
        passive=DealDamagePassive(
            name="피의 포식",
            effects=[
                AddStatusEffect(
                    status_class=BleedStatus,
                    status_kwargs={"stack": 3},
                ),
                RestoreHpEffect(
                    power=0.3,
                    stat="attack",
                    target_type="self",
                ),
            ],
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [피에 굶주린 일격]: ATK × 1.5 + 1d10\n"
            "패시브 [피의 포식]: 공격 적중 시 출혈 3 부여 / ATK의 30%만큼 HP 회복\n"
            "아무리 많은 피를 머금어도 갈증이 가시지 않는 대검. 베어낸 생명을 삼켜 주인의 상처를 메운다."
        ),
    ),
    Weapon(
        name="붕괴의 대검",
        hp=15,
        attack=10,
        speed=-3,
        price=200,
        basic_attack=Action(
            name="붕괴",
            effects=[
                DamageEffect(
                    power=2.5,
                    stat="attack",
                    dice_count=1,
                    dice_sides=12,
                ),
                AddStatusEffect(
                    status_class=VulnerableStatus,
                    status_kwargs={
                        "power": 0.5,
                        "duration": 3,
                    },
                ),
                AddStatusEffect(
                    status_class=WeakenStatus,
                    status_kwargs={
                        "power": 0.2,
                        "duration": 3,
                    },
                ),
            ],
            flavor_text="압도적인 일격으로 적을 내리쳐 완전히 무너뜨렸다!",
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [붕괴]: ATK × 2.5 + 1d12 / 취약 50% 부여 (3턴) / 약화 20% 부여 (3턴)\n"
            "모든 것을 힘으로 무너뜨리는 거대한 대검."
        ),
    ),
    Weapon(
        name="무간의 쌍단도",
        attack=5,
        speed=8,
        critical=0.15,
        price=200,
        basic_attack=Action(
            name="무간연격",
            effects=[
                DamageEffect(
                    power=0.35,
                    stat="speed",
                    dice_count=1,
                    dice_sides=4,
                ),
                DamageEffect(
                    power=0.35,
                    stat="speed",
                    dice_count=1,
                    dice_sides=4,
                ),
                DamageEffect(
                    power=0.35,
                    stat="speed",
                    dice_count=1,
                    dice_sides=4,
                ),
                DamageEffect(
                    power=0.35,
                    stat="speed",
                    dice_count=1,
                    dice_sides=4,
                ),
                DamageEffect(
                    power=0.35,
                    stat="speed",
                    dice_count=1,
                    dice_sides=4,
                ),
            ],
            flavor_text="두 자루의 단도로 빈틈없이 적을 난도질했다!",
        ),
        passive=DealDamagePassive(
            name="무간의 흐름",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=7,
                    target_type="self",
                ),
            ],
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [무간연격]: SPD × 0.35 + 1d4 (×5회)\n"
            "패시브 [무간의 흐름]: 공격 적중 시 행동 게이지 +7\n"
            "한 번 휘두르기 시작하면 검격 사이의 빈틈조차 사라지는 기묘한 한 쌍의 단도."
        ),
    ),
    Weapon(
        name="독아",
        attack=4,
        speed=6,
        critical=0.15,
        price=200,
        basic_attack=Action(
            name="사독연섬",
            effects=[
                DamageEffect(
                    power=0.8,
                    stat="speed",
                    dice_count=1,
                    dice_sides=4,
                ),
                DamageEffect(
                    power=0.8,
                    stat="speed",
                    dice_count=1,
                    dice_sides=4,
                ),
                PoisonBurstEffect(),
            ],
            flavor_text="적을 빠르게 두 번 베어낸 뒤, 축적된 독을 터뜨렸다!",
        ),
        passive=DealDamagePassive(
            name="독혈",
            effects=[
                AddStatusEffect(
                    status_class=PoisonStatus,
                    status_kwargs={"stack": 3},
                ),
            ],
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [사독연섬]: SPD × 0.8 + 1d4 (×2회) + 축적된 독 스택만큼 데미지\n"
            "패시브 [독혈]: 공격 적중 시 독 3 부여\n"
            "치명적인 극독이 스며든 한 쌍의 단도. 베어낸 상처에 쌓인 독마저 무기로 삼는다."
        ),
    ),
    Weapon(
        name="자멸의 마검",
        attack=10,
        magic=10,
        price=200,
        damage_dealt_multiplier=1,
        damage_taken_multiplier=1,
        basic_attack=Action(
            name="자멸의 참격",
            effects=[
                DamageEffect(
                    power=0.7,
                    stat="attack",
                    dice_count=1,
                    dice_sides=6,
                ),
                DamageEffect(
                    power=0.7,
                    stat="magic",
                    dice_count=1,
                    dice_sides=6,
                ),
            ],
            flavor_text="마검에 힘과 마력을 쏟아부어 적을 베어냈다!",
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [자멸의 참격]: ATK × 0.7 + 1d6 / MAG × 0.7 + 1d6\n"
            "패시브 [파멸의 저주]: 가하는 데미지 2배 / 받는 데미지 2배\n"
            "소유자의 육신을 대가로 힘과 마력을 한계 이상으로 끌어내는 저주받은 마검."
        ),
    ),
    Weapon(
        name="홍련의 지팡이",
        mp=15,
        magic=10,
        price=200,
        basic_attack=Action(
            name="홍련의 세례",
            effects=[
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                    target_type="all_enemies",
                ),
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                    target_type="all_enemies",
                ),
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                    target_type="all_enemies",
                ),
            ],
            flavor_text="홍련의 불꽃을 연달아 쏟아부어 모든 적을 불태웠다!",
        ),
        passive=DealDamagePassive(
            name="홍련",
            effects=[
                AddStatusEffect(
                    status_class=BurnStatus,
                    status_kwargs={
                        "power": 3,
                        "duration": 3,
                    },
                ),
            ],
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [홍련의 세례]: 모든 적에게 MAG × 0.3 + 1d3 (×3회)\n"
            "패시브 [홍련]: 공격 적중 시 화상 3 부여 (3턴)\n"
            "꺼지지 않는 홍련의 불꽃을 품은 지팡이. 작열하는 불꽃이 전장을 집어삼킨다."
        ),
    ),
    Weapon(
        name="영구빙정의 지팡이",
        mp=15,
        magic=10,
        price=200,
        basic_attack=Action(
            name="빙정 연사",
            effects=[
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                ),
                DamageEffect(
                    power=0.3,
                    stat="magic",
                    dice_count=1,
                    dice_sides=3,
                ),
            ],
            flavor_text="얼어붙은 마력의 결정을 연달아 쏘아 적을 꿰뚫었다!",
        ),
        passive=DealDamagePassive(
            name="영구동토",
            effects=[
                AddStatusEffect(
                    status_class=ColdStatus,
                    status_kwargs={
                        "stack": 3,
                    },
                ),
            ],
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [빙정 연사]: MAG × 0.3 + 1d3 (×3회)\n"
            "패시브 [영구동토]: 공격 적중 시 냉기 3 부여\n"
            "영원히 녹지 않는 마력의 결정을 품은 지팡이. 그 냉기는 닿는 모든 것을 얼어붙게 한다."
        ),
    ),
    Weapon(
        name="불락의 대방패",
        defense=12,
        hp=10,
        speed=-3,
        price=200,

        basic_attack=Action(
            name="성벽 돌진",
            effects=[
                DamageEffect(
                    power=0.8,
                    stat="defense",
                    dice_count=1,
                    dice_sides=10,
                ),
                AddStatusEffect(
                    status_class=CounterStatus,
                    status_kwargs={
                        "power": 1.4,
                        "stat": "defense",
                        "dice_count": 1,
                        "dice_sides": 10,
                    },
                    target_type="self",
                ),
            ],
            flavor_text="거대한 대방패로 적을 짓누르고 반격 태세를 취했다!",
        ),
        passive=TakeDamagePassive(
            name="보복의 가시",
            effects=[
                DamageEffect(
                    power=0.4,
                    stat="defense",
                    dice_count=1,
                    dice_sides=3,
                ),
            ],
        ),

        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [성벽 돌진]: DEF × 0.8 + 1d10 / 반격: DEF × 1.4 + 1d10\n"
            "패시브 [보복의 가시]: 피격 시 DEF × 0.4 + 1d3 데미지\n"
            "무너지지 않는 성벽을 연상시키는 거대한 방패. 공격을 받아낼수록 상대가 더 큰 대가를 치르게 만든다."
        ),
    ),
    Weapon(
        name="파성의 철퇴",
        defense=12,
        hp=10,
        speed=-3,
        price=200,
        basic_attack=Action(
            name="파성격",
            effects=[
                DamageEffect(
                    power=1.2,
                    stat="block",
                    dice_count=1,
                    dice_sides=10,
                ),
                ConsumeBlockEffect(power=1),
            ],
            flavor_text="축적한 모든 방어를 한 점에 집중해 적을 짓뭉갰다!",
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [파성격]: 방어도 × 1.2 + 1d10 / 현재 방어도 전부 소모\n"
            "성벽조차 일격에 무너뜨린다는 거대한 철퇴. 축적한 방어를 파괴적인 힘으로 전환한다."
        ),
    ),
    Weapon(
        name="검 튕기는 변태의 도",
        attack=8,
        speed=6,
        basic_attack=Action(
            name="패링 각이 안 나와",
            effects=[
                DamageEffect(
                    power=1.2,
                    stat="attack",
                    dice_count=1,
                    dice_sides=10,
                ),
            ],
            flavor_text="패링 각이 안 나와서 어쩔 수 없이 평타를 쳤다!",
        ),
        passive=ParrySuccessPassive(
            name="앞잡 들어간다잉",
            effects=[
                DamageEffect(
                    power=1.0,
                    stat="attack",
                    dice_count=1,
                    dice_sides=8,
                ),
                DamageEffect(
                    power=1.0,
                    stat="attack",
                    dice_count=1,
                    dice_sides=8,
                ),
            ],
        ),
        price=200,
        rarity=LEGENDARY,
        flavor_text=(
            "기본 공격 [패링 각이 안 나와]: ATK × 1.2 + 1d10\n"
            "패시브 [앞잡 들어간다잉]: 패링 성공 시 ATK × 1.0 + 1d8 추가타 (×2회)\n"
            "제작자의 취향이 지나치게 반영된 괴상한 도. 공격보다 패링 성공 순간에 더 큰 만족감을 준다."
        ),
    ),
]

armors = [
    # 커먼 방어구
    Armor(
        name="가죽 갑옷",
        hp=5,
        defense=3,
        price=60,
        defense_action=Action(
            name="방어 자세",
            effects=[BlockEffect(power=0.8, flat=3)],
            flavor_text="가죽 갑옷을 고쳐 입어 몸을 보호했다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "방어 [방어 자세]: 방어도 DEF × 0.8 + 3 획득\n"
            "가죽을 덧대 방어력을 높인 평범한 갑옷이다."
        ),
    ),
    Armor(
        name="로브",
        mp=5,
        magic=2,
        price=55,
        defense_action=Action(
            name="마력 방벽",
            effects=[
                BlockEffect(
                    power=0.8,
                    stat="magic",
                ),
            ],
            flavor_text="마력을 펼쳐 몸을 감싸는 방벽을 만들어냈다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "방어 [마력 방벽]: 방어도 MAG × 0.8 획득\n"
            "마력을 보호막으로 전환하는 기초적인 로브."
        ),
    ),
    Armor(
        name="경량복",
        speed=1,
        price=50,
        defense_action=Action(
            name="회피 자세",
            effects=[
                BlockEffect(
                    power=0.8,
                    stat="defense",
                ),
                AddStatusEffect(
                    status_class=DodgeStatus,
                    status_kwargs={
                        "count": 1,
                    },
                    target_type="self",
                ),
            ],
            flavor_text="몸을 낮추고 공격에 대비해 회피 태세를 취했다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "방어 [회피 자세]: 방어도 DEF × 0.8 획득 / 회피 1 획득\n"
            "움직임을 방해하지 않도록 만들어진 가벼운 옷이다."
        ),
    ),
    Armor(
        name="중갑",
        hp=10,
        defense=4,
        speed=-1,
        price=80,
        defense_action=Action(
            name="방어 태세",
            effects=[
                BlockEffect(
                    power=1.2,
                    stat="defense",
                    flat=3,
                    target_type="self",
                )
            ],
            flavor_text="무거운 갑옷으로 몸을 굳건히 지켰다!",
        ),
        passive=BattleStartPassive(
            name="중갑 방어",
            effects=[
                BlockEffect(
                    power=0,
                    flat=10,
                ),
            ],
        ),
        rarity=COMMON,
        flavor_text=(
            "방어 [방어 태세]: 방어도 DEF × 1.2 + 3 획득\n"
            "패시브 [중갑 방어]: 전투 시작 시 방어도 10 획득\n"
            "두꺼운 갑옷. 움직이기는 불편하지만 믿음직스럽다."
        ),
    ),
    Armor(
        name="철 갑옷",
        hp=8,
        defense=5,
        price=80,
        defense_action=Action(
            name="철벽",
            effects=[
                BlockEffect(power=1.1),
            ],
            flavor_text="철제 갑옷으로 공격을 굳건히 받아냈다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "방어 [철벽]: 방어도 DEF × 1.1 획득\n"
            "무겁지만 든든한 철제 갑옷."
        ),
    ),
    Armor(
        name="모험가의 외투",
        hp=3,
        mp=3,
        speed=1,
        defense=1,
        price=75,
        defense_action=Action(
            name="응급 정비",
            effects=[
                BlockEffect(power=0.8),
                RestoreHpEffect(power=0, flat=2),
            ],
            flavor_text="급히 장비를 정비하며 상처를 추슬렀다!",
        ),
        rarity=COMMON,
        flavor_text=(
            "방어 [응급 정비]: 방어도 DEF × 0.8 획득 / HP 2 회복\n"
            "여러 위험에 대처할 수 있도록 만들어진 튼튼한 외투."
        ),
    ),
    Armor(
        name="검객의 외투",
        hp=3,
        speed=2,
        price=70,
        defense_action=Action(
            name="자세 잡기",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=50,
                    target_type="self",
                ),
            ],
            flavor_text="호흡을 가다듬고 다음 움직임을 준비했다!",
        ),
        passive=ParrySuccessPassive(
            name="호흡",
            effects=[
                RestoreMpEffect(
                    power=0,
                    flat=2,
                    target_type="self",
                ),
            ],
        ),
        rarity=COMMON,
        flavor_text=(
            "방어 [자세 잡기]: 행동 게이지 +50\n"
            "패시브 [호흡]: 패링 성공 시 MP 2 회복\n"
            "상대의 공격을 받아치는 순간에도 호흡을 흐트러뜨리지 않도록 만들어진 가벼운 외투."
        ),
    ),
    
    # 레어 방어구
    Armor(
        name="마도복",
        mp=8,
        magic=4,
        price=85,
        defense_action=Action(
            name="마력 방벽",
            effects=[
                BlockEffect(
                    power=1.5,
                    stat="magic",
                ),
            ],
            flavor_text="마력을 집중해 강력한 방벽을 펼쳤다!",
        ),
        passive=SkillUsePassive(
            name="마력 보호막",
            effects=[
                BlockEffect(
                    power=0.3,
                    stat="magic",
                    target_type="self",
                ),
            ],
        ),
        rarity=RARE,
        flavor_text=(
            "방어 [마력 방벽]: 방어도 MAG × 1.5 획득\n"
            "패시브 [마력 보호막]: 스킬 사용 시 방어도 MAG × 0.3 획득\n"
            "마력을 보호막으로 전환하도록 만들어진 전투용 의복."
        ),
    ),
    Armor(
        name="도적의 의복",
        speed=3,
        defense=1,
        price=85,
        defense_action=Action(
            name="회피 기동",
            effects=[
                BlockEffect(
                    power=1.0,
                    stat="defense",
                ),
                AddStatusEffect(
                    status_class=DodgeStatus,
                    status_kwargs={
                        "count": 2,
                    },
                    target_type="self",
                ),
            ],
            flavor_text="몸을 낮추고 공격을 흘려낼 태세를 취했다!",
        ),
        rarity=RARE,
        flavor_text=(
            "방어 [회피 기동]: 방어도 DEF × 1.0 획득 / 회피 2 획득\n"
            "가볍고 유연한 소재로 만들어진 전투용 의복."
        ),
    ),
    Armor(
        name="전사의 갑옷",
        hp=7,
        attack=3,
        defense=2,
        price=95,
        defense_action=Action(
            name="버티기",
            effects=[
                BlockEffect(power=1),
                RestoreHpEffect(
                    power=0.1,
                    flat=2,
                    stat="attack",
                    target_type="self",
                ),
            ],
            flavor_text="공격을 정면으로 받아내며 상처를 추슬렀다!",
        ),
        passive=TakeDamagePassive(
            name="투지",
            effects=[
                RestoreHpEffect(
                    power=0.1,
                    stat="attack",
                    target_type="self",
                ),
            ],
        ),
        rarity=RARE,
        flavor_text=(
            "방어 [버티기]: 방어도 DEF × 1.0 획득 / HP ATK × 0.1 + 2 회복\n"
            "패시브 [투지]: 피격 시 HP ATK × 0.1 회복\n"
            "정면에서 공격을 받아내며 싸우도록 만들어진 갑옷."
        ),
    ),
    Armor(
        name="강화 중갑",
        hp=10,
        defense=6,
        speed=-2,
        price=95,
        defense_action=Action(
            name="철벽 자세",
            effects=[
                BlockEffect(
                    power=1.4,
                    stat="defense",
                    flat=3,
                    target_type="self",
                ),
            ],
            flavor_text="단단히 자세를 잡아 공격을 받아낼 준비를 마쳤다!",
        ),
        passive=[
            BattleStartPassive(
                name="중장 방어",
                effects=[
                    BlockEffect(
                        power=0,
                        flat=15,
                        target_type="self",
                    ),
                ],
            ),
            TurnStartPassive(
                name="철벽",
                effects=[
                    BlockEffect(
                        power=0.25,
                        stat="defense",
                        target_type="self",
                    ),
                ],
            ),
        ],
        rarity=RARE,
        flavor_text=(
            "방어 [철벽 자세]: 방어도 DEF × 1.4 + 3 획득\n"
            "패시브 [중장 방어]: 전투 시작 시 방어도 15 획득\n"
            "패시브 [철벽]: 턴 시작 시 방어도 DEF × 0.25 획득\n"
            "두꺼운 금속판을 겹겹이 덧댄 중갑."
        ),
    ),
    Armor(
        name="검사의 외투",
        speed=3,
        defense=2,
        defense_action=Action(
            name="호흡 가다듬기",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=75,
                    target_type="self",
                ),
            ],
            flavor_text="호흡을 가다듬으며 다음 움직임을 준비했다!",
        ),
        passive=ParrySuccessPassive(
            name="정교한 호흡",
            effects=[
                RestoreMpEffect(
                    power=0,
                    flat=3,
                    target_type="self",
                ),
            ],
        ),
        price=95,
        rarity=RARE,
        flavor_text=(
            "방어 [호흡 가다듬기]: 행동 게이지 +75\n"
            "패시브 [정교한 호흡]: 패링 성공 시 MP 3 회복\n"
            "검객의 움직임을 방해하지 않도록 가볍게 제작된 외투."
        ),
    ),
    
    # 에픽 방어구
    Armor(
        name="광전사의 갑옷",
        hp=7,
        attack=7,
        defense=-2,
        price=120,
        defense_action=Action(
            name="맞받아치기",
            effects=[
                BlockEffect(power=0.7),
                RestoreHpEffect(
                    power=0.1,
                    flat=1,
                    stat="attack",
                    target_type="self",
                ),
                AddStatusEffect(
                    status_class=CounterStatus,
                    status_kwargs={"power": 0.5},
                    target_type="self",
                ),
            ],
            flavor_text="공격을 정면으로 받아내며 반격 태세를 취했다!",
        ),
        passive=TakeDamagePassive(
            name="광전",
            effects=[
                RestoreHpEffect(
                    power=0.1,
                    flat=1,
                    stat="attack",
                    target_type="self",
                ),
                AddStatusEffect(
                    status_class=StrengthenStatus,
                    status_kwargs={
                        "power": 0.15,
                        "duration": 2,
                    },
                    target_type="self",
                ),
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "방어 [맞받아치기]: 방어도 DEF × 0.7 획득 / HP ATK × 0.1 + 1 회복 / 반격: ATK × 0.5 + 1d6\n"
            "패시브 [광전]: 피격 시 HP ATK × 0.1 + 1 회복 / 강화 15% 부여 (2턴)\n"
            "상처 입는 것을 두려워하지 않는 전사를 위한 갑옷."
        ),
    ),
    Armor(
        name="성기사의 갑옷",
        hp=15,
        defense=8,
        speed=-3,
        price=140,
        defense_action=Action(
            name="성역 자세",
            effects=[
                BlockEffect(
                    power=1.6,
                    stat="defense",
                    flat=3,
                    target_type="self",
                ),
            ],
            flavor_text="굳건히 자세를 잡아 공격을 받아낼 준비를 마쳤다!",
        ),
        passive=[
            BattleStartPassive(
                name="성스러운 수호",
                effects=[
                    BlockEffect(
                        power=0,
                        flat=20,
                        target_type="self",
                    ),
                ],
            ),
            TurnStartPassive(
                name="불굴의 수호",
                effects=[
                    BlockEffect(
                        power=0.5,
                        stat="defense",
                        target_type="self",
                    ),
                ],
            ),
        ],
        rarity=EPIC,
        flavor_text=(
            "방어 [성역 자세]: 방어도 DEF × 1.6 + 3 획득\n"
            "패시브 [성스러운 수호]: 전투 시작 시 방어도 20 획득\n"
            "패시브 [불굴의 수호]: 턴 시작 시 방어도 DEF × 0.5 획득\n"
            "성기사들이 사용하는 무겁고 견고한 갑옷."
        ),
    ),
    Armor(
        name="달인의 외투",
        hp=5,
        speed=4,
        defense=2,
        defense_action=Action(
            name="간보기",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=100,
                    target_type="self",
                ),
            ],
            flavor_text="상대의 움직임을 살피며 다음 순간을 노렸다!",
        ),
        passive=ParrySuccessPassive(
            name="집중의 호흡",
            effects=[
                RestoreHpEffect(
                    power=0,
                    flat=3,
                    target_type="self",
                ),
                RestoreMpEffect(
                    power=0,
                    flat=4,
                    target_type="self",
                ),
            ],
        ),
        price=140,
        rarity=EPIC,
        flavor_text=(
            "방어 [간보기]: 행동 게이지 +100\n"
            "패시브 [집중의 호흡]: 패링 성공 시 HP 3 / MP 4 회복\n"
            "상대의 움직임을 읽는 데 집중할 수 있도록 만들어진 가벼운 외투."
        ),
    ),
    Armor(
        name="마도사의 예복",
        mp=12,
        magic=6,
        price=140,
        defense_action=Action(
            name="고밀도 마력 방벽",
            effects=[
                BlockEffect(
                    power=2.0,
                    stat="magic",
                ),
            ],
            flavor_text="고밀도의 마력을 펼쳐 강력한 방벽을 만들어냈다!",
        ),
        passive=SkillUsePassive(
            name="마력 장막",
            effects=[
                BlockEffect(
                    power=0.5,
                    stat="magic",
                    target_type="self",
                ),
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "방어 [고밀도 마력 방벽]: 방어도 MAG × 2.0 획득\n"
            "패시브 [마력 장막]: 스킬 사용 시 방어도 MAG × 0.5 획득\n"
            "고밀도의 마력을 안정적으로 유지하도록 만들어진 예복."
        ),
    ),
    Armor(
        name="그림자의 의복",
        speed=5,
        defense=2,
        price=150,
        defense_action=Action(
            name="그림자 기동",
            effects=[
                BlockEffect(
                    power=1.2,
                    stat="defense",
                ),
                AddStatusEffect(
                    status_class=DodgeStatus,
                    status_kwargs={"count": 2},
                    target_type="self",
                ),
            ],
            flavor_text="그림자처럼 몸을 움직여 공격을 흘려낼 태세를 취했다!",
        ),
        rarity=EPIC,
        flavor_text=(
            "방어 [그림자 기동]: 방어도 DEF × 1.2 획득 / 회피 2 획득\n"
            "착용자의 움직임을 따라 흐르듯 움직이는 가벼운 전투복."
        ),
    ),
    
    # 레전더리 방어구
    Armor(
        name="수라의 갑주",
        hp=15,
        attack=10,
        price=200,
        defense_action=Action(
            name="피의 반격",
            effects=[
                BlockEffect(power=0.7),
                RestoreHpEffect(
                    power=0.15,
                    flat=2,
                    stat="attack",
                    target_type="self",
                ),
                AddStatusEffect(
                    status_class=CounterStatus,
                    status_kwargs={"power": 0.8},
                    target_type="self",
                ),
            ],
            flavor_text="공격을 정면으로 받아내며 강력한 반격 태세를 취했다!",
        ),
        passive=TakeDamagePassive(
            name="수라도",
            effects=[
                RestoreHpEffect(
                    power=0.15,
                    flat=2,
                    stat="attack",
                    target_type="self",
                ),
                AddStatusEffect(
                    status_class=StrengthenStatus,
                    status_kwargs={
                        "power": 0.25,
                        "duration": 2,
                    },
                    target_type="self",
                ),
            ],
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "방어 [피의 반격]: 방어도 DEF × 0.7 획득 / HP ATK × 0.15 + 2 회복 / 반격: ATK × 0.8 + 1d6\n"
            "패시브 [수라도]: 피격 시 HP ATK × 0.15 + 2 회복 / 강화 25% 부여 (2턴)\n"
            "상처를 입을수록 더욱 흉포해지는 전사의 갑주."
        ),
    ),
    Armor(
        name="성채의 갑주",
        hp=20,
        defense=10,
        speed=-4,
        price=200,
        defense_action=Action(
            name="성채 자세",
            effects=[
                BlockEffect(
                    power=2.0,
                    stat="defense",
                    flat=3,
                    target_type="self",
                ),
            ],
            flavor_text="흔들림 없이 자세를 굳혀 공격을 받아냈다!",
        ),
        passive=[
            BattleStartPassive(
                name="완전 방비",
                effects=[
                    BlockEffect(
                        power=0,
                        flat=25,
                        target_type="self",
                    ),
                ],
            ),
            TurnStartPassive(
                name="성채",
                effects=[
                    BlockEffect(
                        power=0.75,
                        stat="defense",
                        target_type="self",
                    ),
                ],
            ),
            TakeDamagePassive(
                name="생명력 회복",
                effects=[
                    RestoreHpEffect(
                        power=0,
                        flat=5,
                        target_type="self",
                    ),
                ],
            ),
        ],
        rarity=LEGENDARY,
        flavor_text=(
            "방어 [성채 자세]: 방어도 DEF × 2.0 + 3 획득\n"
            "패시브 [완전 방비]: 전투 시작 시 방어도 25 획득\n"
            "패시브 [성채]: 턴 시작 시 방어도 DEF × 0.75 획득\n"
            "패시브 [생명력 회복]: 피격 시 HP 5 회복\n"
            "그 자체로 움직이는 성채라 불리는 중갑."
        ),
    ),
    Armor(
        name="대마도사의 로브",
        mp=20,
        magic=8,
        price=200,
        defense_action=Action(
            name="대마력 방벽",
            effects=[
                BlockEffect(
                    power=2.5,
                    stat="magic",
                ),
            ],
            flavor_text="막대한 마력을 펼쳐 거대한 방벽을 만들어냈다!",
        ),
        passive=SkillUsePassive(
            name="마력 장벽",
            effects=[
                BlockEffect(
                    power=0.8,
                    stat="magic",
                    target_type="self",
                ),
            ],
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "방어 [대마력 방벽]: 방어도 MAG × 2.5 획득\n"
            "패시브 [마력 장벽]: 스킬 사용 시 방어도 MAG × 0.8 획득\n"
            "대마도사의 마력을 방벽으로 전환하도록 짜인 최고급 로브."
        ),
    ),
    Armor(
        name="질풍의 의복",
        speed=7,
        defense=3,
        price=200,
        defense_action=Action(
            name="바람걸음",
            effects=[
                BlockEffect(
                    power=1.4,
                    stat="defense",
                ),
                AddStatusEffect(
                    status_class=DodgeStatus,
                    status_kwargs={"count": 3},
                    target_type="self",
                ),
            ],
            flavor_text="바람처럼 몸을 움직여 공격을 흘려낼 태세를 취했다!",
        ),
        passive=TurnEndPassive(
            name="잔상",
            effects=[
                AddStatusEffect(
                    status_class=DodgeStatus,
                    status_kwargs={"count": 1},
                    target_type="self",
                ),
            ],
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "방어 [바람걸음]: 방어도 DEF × 1.4 획득 / 회피 3 획득\n"
            "패시브 [잔상]: 턴 종료 시 회피 1 획득\n"
            "착용자의 움직임을 질풍처럼 가볍게 만드는 의복."
        ),
    ),
    Armor(
        name="검 튕기는 변태의 코트",
        hp=8,
        speed=5,
        defense=3,
        defense_action=Action(
            name="패링 각 재기",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=150,
                    target_type="self",
                ),
            ],
            flavor_text="패링 각이 나올 때까지 상대의 움직임을 지켜봤다!",
        ),
        passive=ParrySuccessPassive(
            name="이 맛에 패링하지",
            effects=[
                RestoreHpEffect(
                    power=0,
                    flat=5,
                    target_type="self",
                ),
                RestoreMpEffect(
                    power=0,
                    flat=5,
                    target_type="self",
                ),
            ],
        ),
        price=200,
        rarity=LEGENDARY,
            flavor_text=(
            "방어 [패링 각 재기]: 행동 게이지 +150\n"
            "패시브 [이 맛에 패링하지]: 패링 성공 시 HP 5 / MP 5 회복\n"
            "제작자의 취향이 지나치게 반영된 괴상한 코트. 공격을 막는 것보다 정확히 튕겨내는 순간을 위해 만들어졌다."
        ),
    ),
]

rings = [
    # 커먼 반지
    Ring(
        name="견고한 의지의 반지",
        hp=5,
        speed=-3,
        defense=2,
        price=70,
        passive=[
            KeepBlockPassive(
                name="견고한 방어",
                power=0.5,
            ),
            TurnStartPassive(
                name="견고한 회복",
                effects=[
                    RestoreHpEffect(
                        power=0,
                        flat=1,
                        target_type="self",
                    ),
                ],
            ),
        ],
        rarity=COMMON,
        flavor_text=(
            "패시브 [견고한 방어]: 턴 시작 시 방어도 50% 유지\n"
            "패시브 [견고한 회복]: 턴 시작 시 HP 1 회복\n"
            "착용자의 의지를 굳건하게 만들어 쉽게 무너지지 않게 하는 반지."
        ),
    ),
    Ring(
        name="전사의 반지",
        hp=3,
        attack=1,
        price=60,
        passive=Passive(
            name="투지",
            attack_bonus=0.1,
            hp_threshold=0.5,
        ),
        rarity=COMMON,
        flavor_text=(
            "패시브 [투지]: HP 50% 이하일 때 ATK 10% 증가\n"
            "상처를 입을수록 투지를 끌어올리는 전사의 반지."
        ),
    ),
    Ring(
        name="마력의 반지",
        mp=5,
        price=60,
        passive=TurnStartPassive(
            name="지속 마력 회복",
            effects=[
                RestoreMpEffect(power=0, flat=2)
            ],
        ),
        rarity=COMMON,
        flavor_text=(
            "패시브 [지속 마력 회복]: 턴 시작 시 MP 2 회복\n"
            "마력을 저장하고 조금씩 되돌려주는 반지."
        ),
    ),
    Ring(
        name="독침의 반지",
        speed=1,
        price=50,
        passive=DealDamagePassive(
            name="독침",
            effects=[
                DamageEffect(
                    power=0,
                    flat=1,
                    can_crit=False,
                    can_trigger_passives=False,
                ),
                AddStatusEffect(
                    status_class=PoisonStatus,
                    status_kwargs={"stack": 1},
                ),
            ],
        ),
        rarity=COMMON,
        flavor_text=(
            "패시브 [독침]: 공격 적중 시 1 데미지 / 독 1 부여\n"
            "미량의 독이 스며든 반지."
        ),
    ),
    Ring(
        name="도전자의 반지",
        attack=1,
        speed=1,
        price=50,
        passive=HpDamagePassive(
            name="오기",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=30,
                    target_type="self",
                ),
            ],
        ),
        rarity=COMMON,
        flavor_text=(
            "패시브 [오기]: HP 피해를 받으면 행동 게이지 +30\n"
            "맞았다고 물러설 이유는 없다."
        ),
    ),
    
    # 레어 반지
    Ring(
        name="주문술사의 반지",
        mp=8,
        magic=2,
        price=80,
        passive=[
            TurnStartPassive(
                name="지속 마력 회복",
                effects=[
                    RestoreMpEffect(
                        power=0,
                        flat=2,
                    ),
                ],
            ),
            SkillUsePassive(
                name="마력 환류",
                effects=[
                    RestoreHpEffect(
                        power=0,
                        flat=3,
                    ),
                ],
            ),
        ],
        rarity=RARE,
        flavor_text=(
            "패시브 [지속 마력 회복]: 턴 시작 시 MP 2 회복\n"
            "패시브 [마력 환류]: 스킬 사용 시 HP 3 회복\n"
            "순환하는 마력을 생명력으로 전환하는 반지."
        ),
    ),
    Ring(
        name="독사의 반지",
        attack=2,
        speed=3,
        price=90,
        passive=DealDamagePassive(
            name="독사의 일격",
            effects=[
                DamageEffect(
                    power=0,
                    flat=2,
                    can_crit=False,
                    can_trigger_passives=False,
                ),
                AddStatusEffect(
                    status_class=PoisonStatus,
                    status_kwargs={"stack": 1},
                ),
            ],
        ),
        rarity=RARE,
        flavor_text=(
            "패시브 [독사의 일격]: 공격 적중 시 2 데미지 / 독 1 부여\n"
            "공격할 때마다 독이 스며드는 반지."
        ),
    ),
    Ring(
        name="불굴의 의지의 반지",
        hp=8,
        defense=3,
        price=110,
        passive=[
            KeepBlockPassive(
                name="불굴의 방어",
                power=0.65,
            ),
            TurnStartPassive(
                name="불굴의 회복",
                effects=[
                    RestoreHpEffect(
                        power=0,
                        flat=2,
                        target_type="self",
                    ),
                ],
            ),
        ],
        rarity=RARE,
        flavor_text=(
            "패시브 [불굴의 방어]: 턴 시작 시 방어도 65% 유지\n"
            "패시브 [불굴의 회복]: 턴 시작 시 HP 2 회복\n"
            "쉽게 꺾이지 않는 의지가 깃든 반지."
        ),
    ),
    Ring(
        name="투사의 반지",
        hp=3,
        attack=3,
        price=90,
        passive=Passive(
            name="투지",
            attack_bonus=0.15,
            hp_threshold=0.5,
        ),
        rarity=RARE,
        flavor_text=(
            "패시브 [투지]: HP 50% 이하일 때 ATK 15% 증가\n"
            "위기에 몰릴수록 투지를 끌어올리는 투사의 반지."
        ),
    ),
    Ring(
        name="승부사의 반지",
        attack=2,
        speed=2,
        passive=ParrySuccessPassive(
            name="재촉",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=30,
                    target_type="attacker",
                ),
            ],
        ),
        price=100,
        rarity=RARE,
        flavor_text=(
            "패시브 [재촉]: 패링 성공 시 공격자의 행동 게이지 +30\n"
            "한 번 공격을 튕겨냈다고 승부가 끝난 것은 아니다."
        ),
    ),
    
    # 에픽 반지
    Ring(
        name="광전사의 반지",
        hp=5,
        attack=5,
        defense=-3,
        price=120,
        passive=Passive(
            name="광전",
            attack_bonus=0.3,
            hp_threshold=0.5,
        ),
        rarity=EPIC,
        flavor_text=(
            "패시브 [광전]: HP 50% 이하일 때 ATK 30% 증가\n"
            "상처와 고통을 투지로 바꾸는 광전사의 반지."
        ),
    ),
    Ring(
        name="현자의 반지",
        mp=12,
        magic=4,
        price=140,
        passive=[
            TurnStartPassive(
                name="지속 마력 회복",
                effects=[
                    RestoreMpEffect(
                        power=0,
                        flat=3,
                    ),
                ],
            ),
            SkillUsePassive(
                name="마력 환류",
                effects=[
                    RestoreHpEffect(
                        power=0,
                        flat=5,
                    ),
                ],
            ),
        ],
        rarity=EPIC,
        flavor_text=(
            "패시브 [지속 마력 회복]: 턴 시작 시 MP 3 회복\n"
            "패시브 [마력 환류]: 스킬 사용 시 HP 5 회복\n"
            "마력의 흐름을 완전히 이해한 자를 위한 반지."
        ),
    ),
    Ring(
        name="살무사의 반지",
        attack=3,
        speed=5,
        price=140,
        passive=DealDamagePassive(
            name="치명적인 독사",
            effects=[
                DamageEffect(
                    power=0,
                    flat=3,
                    can_crit=False,
                    can_trigger_passives=False,
                ),
                AddStatusEffect(
                    status_class=PoisonStatus,
                    status_kwargs={"stack": 2},
                ),
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "패시브 [치명적인 독사]: 공격 적중 시 3 데미지 / 독 2 부여\n"
            "수많은 암살자의 손을 거쳐 완성된 맹독의 반지."
        ),
    ),
    Ring(
        name="도박사의 반지",
        speed=5,
        critical=0.3,
        damage_taken_multiplier=0.15,
        price=95,
        passive=TurnEndPassive(
            name="도박수",
            effects=[
                ActionGaugeEffect(power=0, flat=20),
            ],
        ),
        rarity=EPIC,
        flavor_text=(
            "패시브 [도박수]: 턴 종료 시 행동 게이지 +30 / 받는 데미지 15% 증가\n"
            "목숨을 판돈으로 걸고 한발 먼저 움직이게 하는 반지."
        ),
    ),
    Ring(
        name="철벽의 의지의 반지",
        hp=10,
        defense=5,
        price=140,
        passive=[
            KeepBlockPassive(
                name="철벽의 방어",
                power=0.8,
            ),
            TurnStartPassive(
                name="철벽의 회복",
                effects=[
                    RestoreHpEffect(
                        power=0,
                        flat=3,
                        target_type="self",
                    ),
                ],
            ),
        ],
        rarity=EPIC,
        flavor_text=(
            "패시브 [철벽의 방어]: 턴 시작 시 방어도 80% 유지\n"
            "패시브 [철벽의 회복]: 턴 시작 시 HP 3 회복\n"
            "철벽과도 같은 의지가 깃든 반지."
        ),
    ),
    Ring(
        name="달인의 반지",
        attack=3,
        speed=3,
        passive=ParrySuccessPassive(
            name="도발",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=40,
                    target_type="attacker",
                ),
                AddStatusEffect(
                    status_class=VulnerableStatus,
                    status_kwargs={
                        "power": 0.25,
                        "duration": 2,
                    },
                    target_type="attacker",
                ),
            ],
        ),
        price=140,
        rarity=EPIC,
        flavor_text=(
            "패시브 [도발]: 패링 성공 시 공격자의 행동 게이지 +40 / 취약 25% 부여 (2턴)\n"
            "공격을 튕겨낸 뒤 드러난 빈틈을 놓치지 않는 검객의 반지."
        ),
    ),
    
    # 레전더리 반지
    Ring(
        name="불멸의 의지의 반지",
        hp=15,
        defense=7,
        price=200,
        passive=[
            KeepBlockPassive(
                name="불멸의 방어",
                power=0.9,
            ),
            TurnStartPassive(
                name="불멸의 회복",
                effects=[
                    RestoreHpEffect(
                        power=0,
                        flat=5,
                        target_type="self",
                    ),
                ],
            ),
        ],
        rarity=LEGENDARY,
        flavor_text=(
            "패시브 [불멸의 방어]: 턴 시작 시 방어도 90% 유지\n"
            "패시브 [불멸의 회복]: 턴 시작 시 HP 5 회복\n"
            "결코 꺾이지 않는 의지가 깃든 반지."
        ),
    ),
    Ring(
        name="무한의 반지",
        mp=20,
        magic=6,
        price=200,
        passive=[
            TurnStartPassive(
                name="지속 마력 회복",
                effects=[
                    RestoreMpEffect(
                        power=0,
                        flat=4,
                    ),
                ],
            ),
            SkillUsePassive(
                name="무한 환류",
                effects=[
                    RestoreHpEffect(
                        power=0,
                        flat=8,
                    ),
                    RestoreMpEffect(
                        power=0,
                        flat=3,
                    ),
                ],
            ),
        ],
        rarity=LEGENDARY,
        flavor_text=(
            "패시브 [지속 마력 회복]: 턴 시작 시 MP 4 회복\n"
            "패시브 [무한 환류]: 스킬 사용 시 HP 8 / MP 3 회복\n"
            "마력과 생명력을 끝없이 순환시키는 전설적인 반지."
        ),
    ),
    Ring(
        name="살의의 반지",
        attack=3,
        speed=3,
        price=200,
        passive=DealDamagePassive(
            name="무한 연격",
            effects=[
                DamageEffect(
                    power=0.1,
                    stat="speed",
                    flat=3,
                    can_crit=False,
                    can_trigger_passives=False,
                ),
                AddStatusEffect(
                    status_class=PoisonStatus,
                    status_kwargs={"stack": 2},
                ),
            ],
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "패시브 [무한 연격]: 공격 적중 시 SPD × 0.1 + 3 데미지 / 독 2 부여\n"
            "공격이 이어질수록 치명적인 상처와 맹독을 남기는 반지."
        ),
    ),
    Ring(
        name="회심의 반지",
        critical=0.9,
        price=200,
        rarity=LEGENDARY,
        flavor_text="결정적인 순간을 놓치지 않게 해주는 반지.",
    ),
    Ring(
        name="파괴의 반지",
        damage_dealt_multiplier=0.4,
        price=200,
        rarity=LEGENDARY,
        flavor_text=(
            "패시브 [파괴 본능]: 가하는 데미지 40% 증가\n"
            "착용자의 모든 공격을 무자비하게 증폭시키는 반지."
        ),
    ),
    Ring(
        name="수라의 반지",
        hp=10,
        attack=8,
        defense=-5,
        price=200,
        passive=Passive(
            name="사투",
            attack_bonus=0.5,
            hp_threshold=0.5,
        ),
        rarity=LEGENDARY,
        flavor_text=(
            "패시브 [사투]: HP 50% 이하일 때 ATK 50% 증가\n"
            "죽음에 가까워질수록 착용자의 투쟁 본능을 극한까지 끌어낸다."
        ),
    ),
    Ring(
        name="검 튕기는 변태의 반지",
        attack=4,
        speed=4,
        passive=ParrySuccessPassive(
            name="또 쳐봐",
            effects=[
                ActionGaugeEffect(
                    power=0,
                    flat=50,
                    target_type="attacker",
                ),
                AddStatusEffect(
                    status_class=VulnerableStatus,
                    status_kwargs={
                        "power": 0.4,
                        "duration": 2,
                    },
                    target_type="attacker",
                ),
                AddStatusEffect(
                    status_class=WeakenStatus,
                    status_kwargs={
                        "power": 0.2,
                        "duration": 2,
                    },
                    target_type="attacker",
                ),
            ],
        ),
        price=200,
        rarity=LEGENDARY,
        flavor_text=(
            "패시브 [또 쳐봐]: 패링 성공 시 공격자의 행동 게이지 +50 / 취약 40% 부여 (2턴) / 약화 20% 부여 (2턴)\n"
            "공격을 튕겨낸 뒤 물러나는 것은 하수의 발상이다. 다시 쳐보라고 재촉한 뒤 후속타조차 연속으로 패링하는 것이 고수다."
        ),
    ),
]

equipments = weapons + armors + rings

skills = [
    # 커먼 스킬
    Action(
        name="강타",
        effects=[
            DamageEffect(
                power=1.5,
                stat="attack",
                dice_count=2,
                dice_sides=8,
            )
        ],
        mp_cost=2,
        price=50,
        rarity=COMMON,
        flavor_text="온 힘을 실어 적의 뚝배기를 강타했다!",
        description=(
            "ATK × 1.5 + 2d8 데미지\n"
            "적의 뚝배기를 강타한다."
        ),
    ),
    Action(
        name="연격",
        effects=[
            DamageEffect(power=0.5, stat="attack", dice_count=1, dice_sides=4,),
            DamageEffect(power=0.5, stat="attack", dice_count=1, dice_sides=4,),
            DamageEffect(power=0.5, stat="attack", dice_count=1, dice_sides=4,),
        ],
        mp_cost=2,
        price=50,
        rarity=COMMON,
        flavor_text="빠르게 무기를 휘둘러 3연격을 날렸다!",
        description=(
            "ATK × 0.5 + 1d4 데미지 (×3회)\n"
            "빠른 연격을 3번 날린다."
        ),
    ),
    Action(
        name="마력탄",
        effects=[
            DamageEffect(power=0.5, stat="magic", dice_count=1, dice_sides=4,),
            DamageEffect(power=0.5, stat="magic", dice_count=1, dice_sides=4,),
            DamageEffect(power=0.5, stat="magic", dice_count=1, dice_sides=4,),
        ],
        mp_cost=3,
        price=50,
        rarity=COMMON,
        flavor_text="응축된 마력탄을 연달아 3개 발사했다!",
        description=(
            "MAG × 0.5 + 1d4 데미지 (×3회)\n"
            "응축된 마력의 덩어리를 3개 발사한다."
        ),
    ),
    Action(
        name="냉기탄",
        effects=[
            DamageEffect(
                power=0.8,
                stat="magic",
                dice_count=1,
                dice_sides=6,
            ),
            AddStatusEffect(
                status_class=ColdStatus,
                status_kwargs={
                    "stack": 2,
                },
            ),
        ],
        mp_cost=2,
        price=55,
        rarity=COMMON,
        flavor_text="차가운 마력탄을 쏘아 적을 얼어붙게 했다!",
        description=(
            "MAG × 0.8 + 1d6 데미지 / 냉기 2 부여\n"
            "차가운 마력탄을 쏘아 적의 움직임을 둔화시킨다."
        ),
    ),
    Action(
        name="독 플라스크",
        effects=[AddStatusEffect(
            status_class=PoisonStatus,
            status_kwargs={"stack": 8,})
        ],
        mp_cost=2,
        price=50,
        rarity=COMMON,
        flavor_text="독이 든 플라스크를 적에게 집어던졌다!",
        description=(
            "독 8 부여\n"
            "독이 든 플라스크를 던져 적을 중독시킨다."
        ),
    ),
    Action(
        name="회피 기동",
        effects=[
            AddStatusEffect(
                status_class=DodgeStatus,
                status_kwargs={"count": 2},
                target_type="self",
            ),
        ],
        mp_cost=2,
        price=50,
        rarity=COMMON,
        flavor_text="재빠르게 몸을 움직였다!",
        description=(
            "회피 2 획득\n"
            "재빠르게 몸을 움직여 이어지는 공격을 회피한다."
        ),
    ),
    Action(
        name="회복",
        effects=[RestoreHpEffect(power=0, flat=15)],
        mp_cost=2,
        price=50,
        rarity=COMMON,
        flavor_text="상처를 가다듬고 체력을 회복했다!",
        description=(
            "HP 15 회복\n"
            "상처를 치료해 체력을 회복한다."
        ),
    ),
    Action(
        name="방패 강타",
        effects=[
            DamageEffect(power=0.8, stat="defense", dice_count=1, dice_sides=6),
            AddStatusEffect(
                status_class=WeakenStatus,
                status_kwargs={
                    "power": 0.2,
                    "duration": 2,
                },
            ),
        ],
        mp_cost=2,
        price=60,
        rarity=COMMON,
        flavor_text="방패를 강하게 부딪쳐 적의 기세를 꺾었다!",
        description=(
            "DEF × 0.8 + 1d6 데미지 / 약화 20% 부여 (2턴)\n"
            "방패로 적을 강타해 공격의 기세를 꺾는다."
        ),
    ),
    Action(
        name="철벽 태세",
        effects=[
            BlockEffect(
                power=1.5,
                flat=5,
            ),
        ],
        mp_cost=2,
        price=70,
        rarity=COMMON,
        flavor_text="자세를 굳히고 철벽같이 공격에 대비했다!",
        description=(
            "방어도 DEF × 1.5 + 5 획득\n"
            "단단히 자세를 잡아 공격에 대비한다."
        ),
    ),
    Action(
        name="화염살",
        effects=[
            DamageEffect(power=0.5, stat="magic", dice_count=1, dice_sides=4, target_type="all_enemies",),
            AddStatusEffect(
                status_class=BurnStatus,
                status_kwargs={"power": 1, "duration": 2},
                target_type="all_enemies",
            )
        ],
        mp_cost=2,
        price=50,
        rarity=COMMON,
        flavor_text="폭발하는 화염의 화살을 쏘아 적들을 불태웠다!",
        description=(
            "모든 적에게 MAG × 0.5 + 1d4 데미지 / 화상 1 부여 (2턴)\n"
            "폭발하는 화염의 화살을 쏘아 적들을 불태운다."
        ),
    ),
    Action(
        name="패링",
        effects=[
            ActionGaugeEffect(
                power=0,
                flat=100,
            ),
            AddStatusEffect(
                status_class=ParryStatus,
                status_kwargs={
                    "power": 2,
                    "flat": 5,
                    "dice_count": 1,
                    "dice_sides": 6,
                    "stat": "attack",
                },
                target_type="self",
            ),
        ],
        mp_cost=1,
        price=55,
        rarity=COMMON,
        flavor_text="적의 공격에 정신을 집중했다!",
        description=(
            "행동 게이지 +100 / 패링 활성화\n"
            "다음 공격 패링 시 ATK × 2.0 + 5 + 1d6 반격\n"
            "패링 실패 시 1턴 간 행동불능 및 취약 50% (2턴)\n"
            "다음 공격을 쳐내고 강력하게 반격한다. 패링에 실패하면 자세가 무너진다."
        ),
    ),
    Action(
        name="도발",
        effects=[
            ActionGaugeEffect(power=0, flat=200, target_type="self"),
            ActionGaugeEffect(power=0, flat=100, target_type="enemy"),
        ],
        mp_cost=1,
        price= 50,
        rarity=COMMON,
        flavor_text="적을 도발하며 어서 덤벼보라고 재촉했다!",
        description=(
            "자신의 행동 게이지 +200 / 적의 행동 게이지 +100\n"
            "적을 도발해 더 빠르게 행동하도록 유도한다."
        ),
    ),
    Action(
        name="휩쓸기",
        effects=[
            DamageEffect(
                power=0.7,
                stat="attack",
                dice_count=1,
                dice_sides=6,
                target_type="all_enemies",
            ),
        ],
        mp_cost=2,
        price=60,
        rarity=COMMON,
        flavor_text="무기를 크게 휘둘러 적들을 한꺼번에 휩쓸었다!",
        description=(
            "모든 적에게 ATK × 0.7 + 1d6 데미지\n"
            "무기를 크게 휘둘러 모든 적을 공격한다."
        ),
    ),

    # 레어 스킬
    Action(
        name="흡혈의 참격",
        effects=[
            DamageEffect(power=1.0, stat="attack", dice_count=1, dice_sides=8),
            AddStatusEffect(
                status_class=RegenerationStatus,
                status_kwargs={
                     "power": 0.3,
                     "flat": 5,
                     "duration": 3,
                },
                target_type="self",
            )
        ],
        mp_cost=3,
        price=50,
        rarity=RARE,
        flavor_text="적을 베어 생명력을 빼앗았다!",
        description=(
            "ATK × 1.0 + 1d8 데미지 / 재생 ATK × 0.3 + 5 부여 (3턴)\n"
            "적의 생명력을 빼앗아 자신의 상처를 서서히 회복한다."
        ),
    ),
    Action(
        name="맹독의 참격",
        effects=[
            DamageEffect(
                power=0.4,
                stat="attack",
                dice_count=1,
                dice_sides=4,
            ),
            AddStatusEffect(
                status_class=PoisonStatus,
                status_kwargs={"stack": 4},
            ),
            MultiplyPoisonEffect(power=1.5),
        ],
        mp_cost=4,
        price=95,
        rarity=RARE,
        flavor_text="맹독을 바른 무기로 적을 깊게 베었다!",
        description=(
            "ATK × 0.4 + 1d4 데미지 / 독 4 부여 / 축적된 독 50% 증가\n"
            "맹독을 바른 무기로 베어내 대상의 독을 더욱 증폭시킨다."
        ),
    ),
    Action(
        name="화염 폭발",
        effects=[
            DamageEffect(
                power=0.8,
                stat="magic",
                dice_count=1,
                dice_sides=6,
                target_type="all_enemies",
            ),
            AddStatusEffect(
                status_class=BurnStatus,
                status_kwargs={
                    "power": 2,
                    "duration": 2,
                },
                target_type="all_enemies",
            ),
        ],
        mp_cost=4,
        price=100,
        rarity=RARE,
        flavor_text="거대한 화염을 폭발시켜 적들을 휩쓸었다!",
        description=(
            "모든 적에게 MAG × 0.8 + 1d6 데미지 / 화상 2 부여 (2턴)\n"
            "거대한 화염을 폭발시켜 모든 적을 불태운다."
        ),
    ),
    Action(
        name="빙결창",
        effects=[
            DamageEffect(
                power=1.0,
                stat="magic",
                dice_count=1,
                dice_sides=6,
            ),
            AddStatusEffect(
                status_class=ColdStatus,
                status_kwargs={
                    "stack": 5,
                },
            ),
        ],
        mp_cost=4,
        price=90,
        rarity=RARE,
        flavor_text="얼음으로 이루어진 창을 적에게 쏘아냈다!",
        description=(
            "MAG × 1.0 + 1d6 데미지 / 냉기 5 부여\n"
            "얼음으로 된 창을 쏘아 대량의 냉기를 쌓는다."
        ),
    ),
    Action(
        name="전투 고양",
        effects=[
            AddStatusEffect(
                status_class=StrengthenStatus,
                status_kwargs={
                    "power": 0.2,
                    "duration": 6,
                },
                target_type="self",
            )
        ],
        mp_cost=3,
        price=100,
        rarity=RARE,
        flavor_text="전투 의지를 한껏 끌어올렸다!",
        description=(
            "강화 20% 부여 (6턴)\n"
            "전투 의지를 끌어올려 모든 스테이터스를 강화한다."
        ),
    ),
    Action(
        name="가속",
        effects=[
            AddStatusEffect(
                status_class=HasteStatus,
                status_kwargs={
                    "power": 0,
                    "flat": 100,
                    "duration": 3,
                },
                target_type="self",
            )
        ],
        mp_cost=5,
        price=110,
        rarity=RARE,
        flavor_text="마력으로 신체의 움직임을 가속했다!",
        description=(
            "턴 종료 시 행동 게이지 +100 (3턴)\n"
            "신체의 움직임을 가속해 연속해서 행동할 기회를 만든다."
        ),
    ),
    Action(
        name="성채 붕괴",
        effects=[
            DamageEffect(power=1.5, stat="block", dice_count=2, dice_sides=6, target_type="all_enemies"),
            ConsumeBlockEffect(power=1),
        ],
        mp_cost=5,
        price=105,
        rarity=RARE,
        flavor_text="쌓아올린 방어를 무너뜨리며 그 힘을 적들에게 쏟아부었다!",
        description=(
            "모든 적에게 현재 방어도 × 1.5 + 2d6 데미지 / 보유 방어도 전부 소모\n"
            "쌓아올린 방어를 무너뜨려 강력한 전체 공격을 가한다."
        ),        
    ),
    Action(
        name="방어진 강화",
        effects=[
            BlockEffect(power=1, stat="block")
        ],
        mp_cost=5,
        price=115,
        rarity=RARE,
        flavor_text="기존 방어진을 더욱 견고하게 보강했다!",
        description=(
            "현재 방어도만큼 방어도 획득\n"
            "방어진을 보강해 현재 방어도를 2배로 만든다."
        ),
    ),
    Action(
        name="마력창",
        effects=[
            DamageEffect(
                power=2.0,
                stat="magic",
                dice_count=2,
                dice_sides=8,
            ),
        ],
        mp_cost=4,
        price=100,
        rarity=RARE,
        flavor_text="응축한 마력의 창으로 적을 꿰뚫었다!",
        description=(
            "MAG × 2.0 + 2d8 데미지\n"
            "마력으로 이루어진 창을 응축해 적 하나를 꿰뚫는다."
        ),
    ),
    Action(
        name="선혈의 참격",
        effects=[
            DamageEffect(
                power=1,
                stat="attack",
                dice_sides=2,
                dice_count=8,
            ),
            AddStatusEffect(
                status_class=BleedStatus,
                status_kwargs={"stack": 7},
            )
        ],
        mp_cost=4,
        price=110,
        rarity=RARE,
        flavor_text="적의 살점을 깊숙이 베어냈다!",
        description=(
            "ATK × 1.0 + 8d2 데미지 / 출혈 7 부여\n"
            "날카롭게 베어 다량의 출혈을 유발한다."
        ),
    ),
    Action(
        name="강격",
        effects=[
            DamageEffect(
                power=1.7,
                stat="attack",
                dice_count=2,
                dice_sides=8,
            ),
            AddStatusEffect(
                status_class=VulnerableStatus,
                status_kwargs={
                    "power": 0.25,
                    "duration": 2,
                },
            ),
        ],
        mp_cost=3,
        price=100,
        rarity=RARE,
        flavor_text="강력한 일격으로 적의 자세를 무너뜨렸다!",
        description=(
            "ATK × 1.7 + 2d8 데미지 / 취약 25% 부여 (2턴)\n"
            "강력한 일격으로 적의 자세를 무너뜨린다."
        ),
    ),
    Action(
        name="연막",
        effects=[
            AddStatusEffect(
                status_class=WeakenStatus,
                status_kwargs={
                    "power": 0.2,
                    "duration": 2,
                },
                target_type="all_enemies",
            ),
            AddStatusEffect(
                status_class=DodgeStatus,
                status_kwargs={
                    "count": 1
                },
                target_type="self",
            )
        ],
        mp_cost=3,
        price=90,
        rarity=RARE,
        flavor_text="주변에 짙은 연막을 터뜨렸다!",
        description=(
            "모든 적에게 약화 20% 부여 (2턴) / 회피 1 획득\n"
            "연막으로 적들의 공격을 방해하고 몸을 숨긴다."
        ),
    ),
    Action(
        name="난무",
        effects=[
            DamageEffect(power=0.1, stat="attack", dice_count=1, dice_sides=3, target_type="all_enemies"),
            DamageEffect(power=0.1, stat="attack", dice_count=1, dice_sides=3, target_type="all_enemies"),
            DamageEffect(power=0.1, stat="attack", dice_count=1, dice_sides=3, target_type="all_enemies"),
            DamageEffect(power=0.1, stat="attack", dice_count=1, dice_sides=3, target_type="all_enemies"),
            DamageEffect(power=0.1, stat="attack", dice_count=1, dice_sides=3, target_type="all_enemies"),
        ],
        mp_cost=4,
        price=85,
        rarity=RARE,
        flavor_text="무기를 미친 듯이 휘둘러 적들을 난도질했다!",
        description=(
            "모든 적에게 ATK × 0.1 + 1d3 데미지 (×5회)\n"
            "무기를 빠르게 휘둘러 모든 적을 연속으로 공격한다."
        ),
    ),
    Action(
        name="납도",
        effects=[
            DamageEffect(
                power=1.5,
                stat="attack",
                dice_count=1,
                dice_sides=8,
            ),
            ActionGaugeEffect(
                power=0,
                flat=-100,
                target_type="self",
            ),
            AddStatusEffect(
                status_class=ParryStatus,
                status_kwargs={
                    "power": 1,
                    "flat": 0,
                    "dice_count": 1,
                    "dice_sides": 6,
                    "stat": "attack",
                },
                target_type="self",
            ),
        ],
        mp_cost=2,
        price=90,
        rarity=RARE,
        flavor_text="적을 베어낸 뒤 검을 거두며 호흡을 가다듬었다!",
        description=(
            "ATK × 1.5 + 1d8 데미지 / 행동 게이지 -100 / 패링 활성화\n"
            "다음 공격 패링 시 ATK × 1.0 + 1d6 반격\n"
            "패링 실패 시 1턴 간 행동불능 및 취약 50% (2턴)\n"
            "적을 베어낸 뒤 검을 거두고 반격의 순간을 기다린다."
        ),
    ),
    Action(
        name="발도",
        effects=[
            DamageEffect(
                power=0.4,
                stat="attack",
                dice_count=1,
                dice_sides=4,
            ),
            ActionGaugeEffect(
                power=0,
                flat=100,
                target_type="self",
            ),
        ],
        mp_cost=2,
        price=90,
        rarity=RARE,
        flavor_text="검을 뽑는 순간 눈앞의 적을 베어냈다!",
        description=(
            "ATK × 0.4 + 1d4 데미지 / 행동 게이지 +100\n"
            "검을 뽑는 순간 적을 베어내며 다음 행동을 앞당긴다."
        ),
    ),
    Action(
        name="독성 발작",
        effects=[
            PoisonBurstEffect(),
        ],
        mp_cost=3,
        price=100,
        rarity=RARE,
        flavor_text="적의 체내에 퍼진 독을 강제로 발작시켰다!",
        description=(
            "축적된 독 스택만큼 데미지\n"
            "체내에 퍼진 독을 자극해 즉시 독성 피해를 일으킨다."
        ),
    ),

    # 에픽 스킬
    Action(
        name="내려찍기",
        effects=[
            DamageEffect(
                power=2,
                stat="attack",
                dice_count=3,
                dice_sides=8,
            ),
            AddStatusEffect(
                status_class=VulnerableStatus,
                status_kwargs={
                    "power": 0.25,
                    "duration": 3,
                },
            ),
        ],
        mp_cost=3,
        price=140,
        rarity=EPIC,
        flavor_text="무기를 온 힘을 다해 적에게 내리찍었다!",
        description=(
            "ATK × 2.0 + 3d8 데미지 / 취약 25% 부여 (3턴)\n"
            "무기를 온 힘을 다해 내리찍어 적의 자세를 무너뜨린다."
        ),
    ),
    Action(
        name="마력 붕괴",
        effects=[
            DamageEffect(
                power=1.2,
                stat="magic",
                dice_count=3,
                dice_sides=8,
                target_type="all_enemies",
            ),
            AddStatusEffect(
                status_class=WeakenStatus,
                status_kwargs={
                    "power": 0.2,
                    "duration": 2,
                },
                target_type="all_enemies",
            ),
        ],
        mp_cost=6,
        price=140,
        rarity=EPIC,
        flavor_text="응축된 마력을 폭발시켜 주변을 휩쓸었다!",
        description=(
            "모든 적에게 MAG × 1.2 + 3d8 데미지 / 약화 20% 부여 (2턴)\n"
            "마력을 폭발시켜 적들의 마력 흐름을 붕괴시킨다."
        ),
    ),
    Action(
        name="불꽃 세례",
        effects=[
            DamageEffect(power=0.2, stat="magic", dice_count=1, dice_sides=4, target_type="all_enemies",),
            AddStatusEffect(
                status_class=BurnStatus,
                status_kwargs={
                    "power": 3,
                    "duration": 3,
                },
                target_type="all_enemies",
            ),
            DamageEffect(power=0.2, stat="magic", dice_count=1, dice_sides=4, target_type="all_enemies",),
            AddStatusEffect(
                status_class=BurnStatus,
                status_kwargs={
                    "power": 3,
                    "duration": 3,
                },
                target_type="all_enemies",
            ),
            DamageEffect(power=0.2, stat="magic", dice_count=1, dice_sides=4, target_type="all_enemies",),
            AddStatusEffect(
                status_class=BurnStatus,
                status_kwargs={
                    "power": 3,
                    "duration": 3,
                },
                target_type="all_enemies",
            ),
        ],
        mp_cost=4,
        price=90,
        rarity=EPIC,
        flavor_text="쏟아지는 불꽃으로 적들을 세 차례 휩쓸었다!",
        description=(
            "모든 적에게 MAG × 0.2 + 1d4 데미지 / 화상 3 부여 (3턴) (×3회)\n"
            "세 번의 불꽃 세례를 퍼부어 화상의 위력을 빠르게 높인다."
        ),
    ),
    Action(
    name="혈화난무",
        effects=[
            DamageEffect(power=0.2, stat="attack", dice_count=1, dice_sides=4, target_type="all_enemies",),
            AddStatusEffect(
                status_class=BleedStatus,
                status_kwargs={
                    "stack": 3,
                },
                target_type="all_enemies",
            ),
            DamageEffect(power=0.2, stat="attack", dice_count=1, dice_sides=4, target_type="all_enemies",),
            AddStatusEffect(
                status_class=BleedStatus,
                status_kwargs={
                    "stack": 3,
                },
                target_type="all_enemies",
            ),
            DamageEffect(power=0.2, stat="attack", dice_count=1, dice_sides=4, target_type="all_enemies",),
            AddStatusEffect(
                status_class=BleedStatus,
                status_kwargs={
                    "stack": 3,
                },
                target_type="all_enemies",
            ),
        ],
        mp_cost=4,
        price=90,
        rarity=EPIC,
        flavor_text="무기를 난폭하게 휘둘러 적들을 세 차례 베어냈다!",
        description=(
            "모든 적에게 ATK × 0.2 + 1d4 데미지 / 출혈 3 부여 (×3회)\n"
            "광역으로 세 차례 베어 출혈을 빠르게 누적시킨다."
        ),
    ),
    Action(
        name="독무",
        effects=[
            AddStatusEffect(
                status_class=PoisonStatus,
                status_kwargs={"stack": 11},
                target_type="all_enemies",
            ),
            AddStatusEffect(
                status_class=WeakenStatus,
                status_kwargs={
                    "power": 0.2,
                    "duration": 3,
                },
                target_type="all_enemies",
            ),
            AddStatusEffect(
                status_class=DodgeStatus,
                status_kwargs={"count": 2},
                target_type="self",
            ),
        ],
        mp_cost=6,
        price=145,
        rarity=EPIC,
        flavor_text="독성 안개를 터뜨려 전장을 뒤덮었다!",
        description=(
            "모든 적에게 독 11 / 약화 20% 부여 (3턴) / 회피 2 획득\n"
            "독성 안개로 적들을 중독시키고 그 틈에 몸을 숨긴다."
        ),
    ),
    Action(
        name="빙정창",
        mp_cost=5,
        effects=[
            DamageEffect(
                power=1.6,
                stat="magic",
                dice_count=2,
                dice_sides=8,
            ),
            AddStatusEffect(
                status_class=ColdStatus,
                status_kwargs={
                    "stack": 6,
                },
            ),
        ],
        price=140,
        rarity=EPIC,
        flavor_text="거대한 얼음의 창을 한 점에 집중시켜 적을 꿰뚫었다!",
        description=(
            "MAG × 1.6 + 2d8 데미지 / 냉기 6 부여\n"
            "거대한 얼음의 창을 한 점에 집중시켜 적을 꿰뚫는다."
        ),
    ),
    Action(
        name="약점 노출",
        effects=[
            ConsumeBlockEffect(
                power=1,
                target_type="enemy",
            ),
            AddStatusEffect(
                status_class=VulnerableStatus,
                status_kwargs={
                    "power": 0.25,
                    "duration": 3,
                },
                target_type="enemy",
            ),
        ],
        mp_cost=4,
        price=145,
        rarity=EPIC,
        flavor_text="적의 방어를 무너뜨려 치명적인 약점을 드러냈다!",
        description=(
            "적의 방어도 전부 제거 / 취약 25% 부여 (3턴)\n"
            "적의 방어를 무너뜨리고 약점을 드러낸다."
        ),
    ),
    Action(
        name="참호 구축",
        effects=[
            BlockEffect(
                power=1,
                flat=5,
            ),
            AddStatusEffect(
                status_class=EntrenchStatus,
                status_kwargs={
                    "power": 0.7,
                    "flat": 0,
                    "duration": 3,
                },
                target_type="self",
            ),
        ],
        mp_cost=5,
        price=140,
        rarity=EPIC,
        flavor_text="자리를 굳히고 견고한 방어진을 구축했다!",
        description=(
            "방어도 DEF × 1.0 + 5 획득 / 피격 시 방어도 DEF × 0.7 획득 (3턴)\n"
            "참호를 구축해 공격받을수록 방어를 더욱 견고하게 만든다."
        ),
    ),
    Action(
        name="성벽 분쇄",
        effects=[
            DamageEffect(
                power=1.5,
                stat="block",
                dice_count=2,
                dice_sides=8,
            ),
            ConsumeBlockEffect(power=0.5),
        ],
        mp_cost=6,
        price=140,
        rarity=EPIC,
        flavor_text="쌓아올린 성벽의 힘을 실어 적을 강타했다!",
        description=(
            "현재 방어도 × 1.5 + 2d8 데미지 / 보유 방어도 50% 소모\n"
            "방어도의 절반을 소모해 성벽을 유지한 채 강력한 일격을 가한다."
        ),
    ),
    Action(
        name="진검승부",
        effects=[
            ActionGaugeEffect(
                power=0,
                flat=100,
                target_type="self",
            ),
            ActionGaugeEffect(
                power=0,
                flat=100,
                target_type="enemy",
            ),
            AddStatusEffect(
                status_class=VulnerableStatus,
                status_kwargs={
                    "power": 1.0,
                    "duration": 2,
                },
                target_type="self",
            ),
            AddStatusEffect(
                status_class=VulnerableStatus,
                status_kwargs={
                    "power": 1.0,
                    "duration": 1,
                },
                target_type="enemy",
            ),
        ],
        mp_cost=2,
        price=140,
        rarity=EPIC,
        flavor_text="적에게 물러설 수 없는 진검승부를 걸었다!",
        description=(
            "자신과 적의 행동 게이지 +100 / 서로 취약 100% 부여\n"
            "서로의 방어를 버리고 다음 일격에 모든 것을 건다."
        ),
    ),
    Action(
        name="횡일섬",
        effects=[
            DamageEffect(
                power=1.5,
                stat="attack",
                dice_count=1,
                dice_sides=8,
                target_type="all_enemies",
            ),
            ActionGaugeEffect(
                power=0,
                flat=-100,
                target_type="self",
            ),
            AddStatusEffect(
                status_class=ParryStatus,
                status_kwargs={
                    "power": 1,
                    "flat": 0,
                    "dice_count": 1,
                    "dice_sides": 6,
                    "stat": "attack",
                },
                target_type="self",
            ),
        ],
        mp_cost=4,
        price=140,
        rarity=EPIC,
        description=(
            "모든 적에게 ATK × 1.5 + 1d8 데미지 / 행동 게이지 -100 / 패링 활성화\n"
            "다음 공격 패링 시 ATK × 1.0 + 1d6 반격\n"
            "패링 실패 시 1턴 간 행동불능 및 취약 50% (2턴)\n"
            "모든 적을 한 번에 베어낸 뒤 반격의 순간을 기다린다. 패링에 실패하면 자세가 무너진다."
        ),
    ),

    # 레전더리 스킬
    Action(
        name="세계",
        effects=[
            ActionGaugeEffect(power=0, flat=1000),
            AddStatusEffect(
                status_class=WorldCooldownStatus,
                status_kwargs={"duration": 11},
                target_type="self",
            ),
        ],
        mp_cost=15,
        price=200,
        rarity=LEGENDARY,
        flavor_text="시간의 흐름을 지배해 혼자만의 세계에 들어섰다!",
        description=(
            "행동 게이지 +1000 / 재사용 대기시간 10턴\n"
            "시간을 지배하여 잠시 동안 혼자만의 세계에 들어선다."
        ),
    ),
    Action(
        name="절대 영도",
        effects=[
            DamageEffect(
                power=1.2,
                stat="magic",
                dice_count=2,
                dice_sides=8,
                target_type="all_enemies",
            ),
            AddStatusEffect(status_class=ColdStatus, status_kwargs={"stack": 7}, target_type="all_enemies",),
        ],
        mp_cost=15,
        price=200,
        rarity=LEGENDARY,
        flavor_text="주변의 모든 열을 빼앗아 전장을 얼어붙게 했다!",
        description=(
            "모든 적에게 MAG × 1.2 + 2d8 데미지 / 냉기 7 부여\n"
            "주변의 모든 열을 빼앗아 전장을 절대 영도에 가깝게 만든다."
        ),
    ),
    Action(
        name="혈제",
        effects=[
            AddStatusEffect(status_class=BleedStatus, status_kwargs={"stack": 15}, target_type="self"),
            DamageEffect(power=0.3, stat="attack", dice_count=1, dice_sides=4, target_type="all_enemies"),
            AddStatusEffect(status_class=BleedStatus, status_kwargs={"stack": 10}, target_type="all_enemies"),
            DamageEffect(power=0.3, stat="attack", dice_count=1, dice_sides=4, target_type="all_enemies"),
            AddStatusEffect(status_class=BleedStatus, status_kwargs={"stack": 10}, target_type="all_enemies"),
            DamageEffect(power=0.3, stat="attack", dice_count=1, dice_sides=4, target_type="all_enemies"),
            AddStatusEffect(status_class=BleedStatus, status_kwargs={"stack": 10}, target_type="all_enemies"),
        ],
        mp_cost=10,
        price=200,
        rarity=LEGENDARY,
        flavor_text="피를 제물로 바쳐 적들을 무자비하게 난도질했다!",
        description=(
            "자신에게 출혈 15 부여\n"
            "모든 적에게 ATK × 0.3 + 1d4 데미지 / 출혈 10 부여 (×3회)\n"
            "자신의 피를 제물로 삼아 모든 적을 난도질하고 막대한 출혈을 일으킨다."
        ),
    ),
    Action(
        name="난공불락",
        effects=[
            AddStatusEffect(
                status_class=FrozenStatus,
                status_kwargs={
                    "duration": 2,
                },
                target_type="self",
            ),
            AddStatusEffect(
                status_class=InvincibleStatus,
                status_kwargs={
                    "duration": 2,
                },
                target_type="self",
            ),
            AddStatusEffect(
                status_class=FortifyStatus,
                status_kwargs={
                    "power": 1.5,
                    "flat": 5,
                    "stat": "defense",
                    "duration": 4,
                },
                target_type="self",
            ),
        ],
        mp_cost=10,
        price=200,
        rarity=LEGENDARY,
        flavor_text="모든 행동을 멈추고 난공불락의 방어 태세에 돌입했다!",
        description=(
            "다음 턴까지 동결 / 무적\n"
            "턴마다 방어도 DEF × 1.5 + 5 획득 (4턴)\n"
            "행동을 포기하는 대신 완전한 방어 태세에 돌입해 공격을 버텨낸다."
        ),
    ),
    Action(
        name="최후의 성벽",
        effects=[
            DamageEffect(
                power=2,
                stat="block",
                dice_count=3,
                dice_sides=10,
                target_type="all_enemies",
            ),
            ConsumeBlockEffect(power=1),
        ],
        mp_cost=10,
        price=200,
        rarity=LEGENDARY,
        flavor_text="쌓아 올린 성벽을 무너뜨려 그 모든 힘을 적들에게 쏟아부었다!",
        description=(
            "모든 적에게 현재 방어도 × 2.0 + 3d10 데미지 / 보유 방어도 전부 소모\n"
            "쌓아 올린 모든 방어도를 무너뜨려 성채의 무게를 적들에게 쏟아붓는다."
        ),
    ),
    Action(
        name="필사의 일격",
        effects=[
            DesperateStrikeEffect(
                power=2,
                stat="attack",
                dice_count=2,
                dice_sides=8,
                hp_cost_power=0.5,
            ),
        ],
        mp_cost=5,
        price=200,
        rarity=LEGENDARY,
        flavor_text="목숨을 내던지듯 온 힘을 실어 필사의 일격을 가했다!",
        description=(
            "현재 HP의 50% 소모 (HP 1 미만으로 감소하지 않음)\n"
            "ATK × 2.0 × (소모 HP / 최대 HP) × 5 + 2d8 데미지\n"
            "현재 체력의 절반을 대가로 필사의 일격을 가한다. 소모하는 체력이 많을수록 위력이 증가한다."
        ),
    ),
    Action(
        name="마력 해방",
        effects=[
            ManaReleaseEffect(
                power=1.5,
                stat="magic",
                dice_count=3,
                dice_sides=8,
                mp_cost_power=1,
                mp_damage_power=3.5,
                target_type="all_enemies",
            ),
            AddStatusEffect(
                status_class=WeakenStatus,
                status_kwargs={
                    "power": 0.4,
                    "duration": 3,
                },
                target_type="all_enemies",
            ),
        ],
        mp_cost=1,
        price=200,
        rarity=LEGENDARY,
        flavor_text="남아 있는 마력을 모조리 해방해 파괴적인 폭발을 일으켰다!",
        description=(
            "남은 MP 전부 소모\n"
            "모든 적에게 MAG × 1.5 + 소모 MP × 3.5 + 3d8 데미지 / 약화 40% 부여 (3턴)\n"
            "남은 마력을 모조리 해방해 모든 적을 파괴적인 폭발에 휩쓴다."
        ),
    ),
    Action(
        name="불멸의 불꽃",
        effects=[
            DamageEffect(
                power=1.0,
                stat="magic",
                dice_count=2,
                dice_sides=8,
                target_type="all_enemies",
            ),
            AddStatusEffect(
                status_class=BurnStatus,
                status_kwargs={
                    "power": 10,
                    "duration": 100,
                },
                target_type="all_enemies",
            ),
        ],
        mp_cost=10,
        price=200,
        rarity=LEGENDARY,
        flavor_text="영원히 타오르는 불꽃을 폭발시켜 적들을 집어삼켰다!",
        description=(
            "모든 적에게 MAG × 1.0 + 2d8 데미지 / 화상 10 부여 (100턴)\n"
            "영원히 타오르는 불꽃으로 모든 적에게 꺼지지 않는 화상을 남긴다."
        ),
    ),
    Action(
        name="촉매",
        effects=[
            MultiplyPoisonEffect(power=2),
            PoisonBurstEffect(),
        ],
        mp_cost=10,
        price=200,
        rarity=LEGENDARY,
        flavor_text="적의 체내에 퍼진 독을 걷잡을 수 없이 폭주시켰다!",
        description=(
            "축적된 독 100% 증가 / 증가한 독 스택만큼 즉시 데미지\n"
            "대상의 독을 2배로 증폭시키고 폭주한 독성을 즉시 발작시킨다."
        ),
    ),
    Action(
        name="그림자 습격",
        effects=[
            AddStatusEffect(
                status_class=DodgeStatus,
                status_kwargs={"count": 4},
                target_type="self",
            ),
            AddStatusEffect(
                status_class=ShadowAssaultStatus,
                status_kwargs={
                    "power": 0.5,
                    "duration": 4,
                },
                target_type="self",
            ),
        ],
        mp_cost=10,
        price=200,
        rarity=LEGENDARY,
        flavor_text="그림자 속으로 몸을 감추며 수많은 잔상을 만들어냈다!",
        description=(
            "회피 4 획득 / 그림자 습격 활성화 (3턴)\n"
            "공격 적중 시 SPD × 0.5 추가 데미지\n"
            "그림자 속에서 적의 공격을 피하며 잔상을 이용해 끊임없이 추가 공격을 가한다."
        ),
    ),
    Action(
        name="히코보시",
        effects=[
            ActionGaugeEffect(
                power=0,
                flat=200,
                target_type="enemy",
            ),
            AddStatusEffect(
                status_class=ParryStatus,
                status_kwargs={
                    "power": 4.0,
                    "flat": 10,
                    "dice_count": 2,
                    "dice_sides": 10,
                    "stat": "attack",
                },
                target_type="self",
            ),
        ],
        mp_cost=5,
        price=200,
        rarity=LEGENDARY,
        flavor_text="별빛을 검끝에 담아 필살의 한 순간을 기다렸다!",
        description=(
            "적의 행동 게이지 +200 / 패링 활성화\n"
            "다음 공격 패링 시 ATK × 4.0 + 10 + 2d10 반격\n"
            "패링 실패 시 1턴 간 행동불능 및 취약 50% (2턴)\n"
            "별빛을 검끝에 담아 적의 행동을 재촉하고, 다가오는 일격에 모든 것을 건다. 패링에 실패하면 자세가 무너진다."
        ),
    ),
    Action(
        name="세츠나",
        effects=[
            ActionGaugeEffect(
                power=0,
                flat=-200
            ),
            AddStatusEffect(
                status_class=AbsoluteParryStatus,
                status_kwargs={
                    "power": 1,
                    "flat": 5,
                    "dice_count": 1,
                    "dice_sides": 6,
                },
                target_type="self",
            ),
        ],
        mp_cost=5,
        price=200,
        rarity=LEGENDARY,
        flavor_text="찰나의 틈새를 포착해 쏟아지는 공격에 정신을 집중했다!",
        description=(
            "행동 게이지 -200 / 절대 패링 활성화\n"
            "다음 턴까지 모든 공격 패링 / 패링 시 ATK × 1.0 + 5 + 1d6 반격\n"
            "패링 실패 시 1턴 간 행동불능 및 취약 50% (2턴)\n"
            "찰나의 틈새를 포착해 다음 턴까지 쏟아지는 모든 공격을 패링한다."
        ),
    ),
]

enemies_first_floor = [
    Enemy(
        name="슬라임",
        max_hp=30,
        speed=10,
        attack=5,
        defense=5,
        gold=30,
        action_pool=[
            Action(
                name="공격",
                effects=[DamageEffect()],
                mp_cost=0,
                flavor_text="슬라임은 당신을 공격했다!",
            ),
            Action(
                name="웅크리기",
                effects=[BlockEffect()],
                mp_cost=0,
                flavor_text="슬라임은 몸을 웅크린다!",
            ),
            Action(
                name="몸통박치기",
                effects=[DamageEffect(power=2)],
                mp_cost=0,
                flavor_text="슬라임의 몸통박치기!",
            ),
        ],
    ),
    Enemy(
        name="고블린",
        max_hp=20,
        speed=13,
        attack=3,
        defense=0,
        gold=20,
        action_pool=[
            Action(
                name="공격",
                effects=[DamageEffect()],
                mp_cost=0,
                flavor_text="고블린은 당신을 공격했다!",
            ),
            Action(
                name="공격",
                effects=[DamageEffect()],
                mp_cost=0,
                flavor_text="고블린은 당신을 공격했다!",
            ),
            Action(
                name="강공격",
                effects=[DamageEffect(power=2.5)],
                mp_cost=0,
                flavor_text="고블린의 강공격!",
            ),
        ],
    ),
    Enemy(
        name="날아다니는 마도서",
        max_hp=30,
        speed=6,
        attack=6,
        magic=10,
        gold=40,
        action_pool=[
            Action(
                name="방어 술식",
                effects=[BlockEffect(power=1.3, stat="magic")],
                mp_cost=0,
                flavor_text="마도서는 방어 술식을 전개했다!",
            ),
            Action(
                name="공격",
                effects=[DamageEffect()],
                mp_cost=0,
                flavor_text="마도서는 당신을 향해 날아들었다!",
            ),
            Action(
                name="회복",
                effects=[RestoreHpEffect(power=0.7)],
                mp_cost=0,
                flavor_text="마도서는 회복 주문을 외웠다!",
            ),
        ],
    ),
    Enemy(
        name="굶주린 늑대",
        max_hp=25,
        speed=20,
        attack=10,
        defense=1,
        gold=35,
        action_pool=[
            Action(
                name="준비1",
                effects=[BlockEffect(power=3)],
                mp_cost=0,
                flavor_text="굶주린 늑대는 굶주렸다!",
            ),
            Action(
                name="준비2",
                effects=[BlockEffect(power=2)],
                mp_cost=0,
                flavor_text="굶주린 늑대는 굶주렸다!!",
            ),
            Action(
                name="준비3",
                effects=[BlockEffect(power=1)],
                mp_cost=0,
                flavor_text="굶주린 늑대는 굶주렸다!!!",
            ),
            Action(
                name="공격",
                effects=[DamageEffect()],
                mp_cost=0,
                flavor_text="굶주린 늑대가 당신을 물어뜯었다!",
            ),
        ],
    ),
    Enemy(
        name="단단한 거북",
        max_hp=50,
        speed=5,
        attack=5,
        defense=5,
        gold=40,
        action_pool=[
            Action(
                name="단단해지기1",
                effects=[BlockEffect(power=1.2)],
                mp_cost=0,
                flavor_text="단단한 거북의 단단해지기! 효과가 별로인 듯하다...",
            ),
            Action(
                name="물 뿜기1",
                effects=[DamageEffect(power=1.7)],
                mp_cost=0,
                flavor_text="단단한 거북의 물 뿜기! 효과가 별로인 듯하다...",
            ),
            Action(
                name="단단해지기2",
                effects=[BlockEffect(power=2.5)],
                mp_cost=0,
                flavor_text="단단한 거북의 단단해지기! 효과가 굉장했다!",
            ),
            Action(
                name="물 뿜기2",
                effects=[DamageEffect(power=3.7)],
                mp_cost=0,
                flavor_text="단단한 거북의 물 뿜기! 효과가 굉장했다!",
            ),
        ],
    ),
    Enemy(
        name="서투른 도적",
        max_hp=24,
        speed=10,
        attack=4,
        defense=2,
        gold=35,
        action_pool=[
            Action(
                name="견제",
                effects=[DamageEffect(power=0.7), BlockEffect(power=0.8)],
                mp_cost=0,
                flavor_text="도적은 당신을 견제하며 거리를 벌렸다!",
            ),
            Action(
                name="공격",
                effects=[DamageEffect()],
                mp_cost=0,
                flavor_text="도적이 단검을 휘둘렀다!",
            ),
            Action(
                name="연속 베기",
                effects=[
                    DamageEffect(power=0.6),
                    DamageEffect(power=0.6),
                    DamageEffect(power=0.6),
                ],
                mp_cost=0,
                flavor_text="도적이 빠르게 단검을 연달아 휘둘렀다!",
            ),
        ],
    ),
    Enemy(
        name="견습 마법사",
        max_hp=22,
        speed=9,
        attack=2,
        magic=8,
        defense=1,
        gold=40,
        action_pool=[
            Action(
                name="마력 보호막",
                effects=[BlockEffect(power=1.5, stat="magic")],
                mp_cost=0,
                flavor_text="견습 마법사가 마력 보호막을 펼쳤다!",
            ),
            Action(
                name="마력탄",
                effects=[
                    DamageEffect(power=0.7, stat="magic"),
                    DamageEffect(power=0.7, stat="magic"),
                ],
                mp_cost=0,
                flavor_text="견습 마법사가 두 발의 마력탄을 발사했다!",
            ),
            Action(
                name="화염구",
                effects=[DamageEffect(power=2.2, stat="magic")],
                mp_cost=0,
                flavor_text="견습 마법사가 화염구를 던졌다!",
            ),
        ],
    ),
    Enemy(
        name="흡혈 박쥐",
        max_hp=20,
        speed=15,
        attack=4,
        magic=5,
        defense=0,
        gold=30,
        action_pool=[
            Action(
                name="할퀴기",
                effects=[
                    DamageEffect(power=0.8)
                ],
                mp_cost=0,
                flavor_text="흡혈 박쥐가 날카로운 발톱으로 할퀴었다!",
            ),
            Action(
                name="흡혈",
                effects=[
                    DamageEffect(power=0.6),
                    RestoreHpEffect(power=0.6, stat="attack"),
                ],
                mp_cost=0,
                flavor_text="흡혈 박쥐가 피를 빨아들였다!",
            ),
            Action(
                name="흡혈",
                effects=[
                    DamageEffect(power=0.6),
                    RestoreHpEffect(power=0.6, stat="attack"),
                ],
                mp_cost=0,
                flavor_text="흡혈 박쥐가 피를 빨아들였다!",
            ),
        ],
    ),
    Enemy(
        name="광전사 오크",
        max_hp=35,
        speed=8,
        attack=5,
        defense=1,
        gold=45,
        action_pool=[
            Action(
                name="휘두르기",
                effects=[DamageEffect(power=1.2)],
                mp_cost=0,
                flavor_text="오크가 무기를 거칠게 휘둘렀다!",
            ),
            Action(
                name="광분",
                effects=[DamageEffect(power=1.7)],
                mp_cost=0,
                flavor_text="오크가 괴성을 지르며 달려들었다!",
            ),
            Action(
                name="분쇄",
                effects=[DamageEffect(power=2.5)],
                mp_cost=0,
                flavor_text="오크가 온 힘을 다해 무기를 내리찍었다!",
            ),
        ],
    ),
    Enemy(
        name="돌 골렘",
        max_hp=55,
        speed=4,
        attack=8,
        defense=7,
        gold=50,
        action_pool=[
            Action(
                name="돌가죽",
                effects=[BlockEffect(power=1.5)],
                mp_cost=0,
                flavor_text="돌 골렘의 표면이 더욱 단단하게 굳어졌다!",
            ),
            Action(
                name="돌가죽",
                effects=[BlockEffect(power=1.2)],
                mp_cost=0,
                flavor_text="돌 골렘이 몸을 웅크리며 힘을 모은다!",
            ),
            Action(
                name="지면 강타",
                effects=[DamageEffect(power=3.0)],
                mp_cost=0,
                flavor_text="돌 골렘이 거대한 주먹으로 지면을 내리쳤다!",
            ),
        ],
    ),
]

enemies_second_floor = [
    Enemy(
        name="독침 거미",
        max_hp=46,
        speed=13,
        attack=4,
        defense=2,
        gold=45,
        action_pool=[
            Action(
                name="물기",
                effects=[
                    DamageEffect(power=0.9),
                ],
                mp_cost=0,
                flavor_text="독침 거미가 날카로운 이빨로 물어뜯었다!",
            ),
            Action(
                name="독침",
                effects=[
                    DamageEffect(power=0.6),
                    AddStatusEffect(
                        status_class=PoisonStatus,
                        status_kwargs={
                            "stack": 2,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="독침 거미가 독이 묻은 침을 찔러 넣었다!",
            ),
            Action(
                name="독액 분사",
                effects=[
                    AddStatusEffect(
                        status_class=PoisonStatus,
                        status_kwargs={
                            "stack": 3,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="독침 거미가 끈적한 독액을 뿜어냈다!",
            ),
        ],
    ),

    Enemy(
        name="화염 임프",
        max_hp=44,
        speed=12,
        attack=3,
        magic=5,
        defense=2,
        gold=45,
        action_pool=[
            Action(
                name="불씨",
                effects=[
                    DamageEffect(
                        power=0.8,
                        stat="magic",
                    ),
                ],
                mp_cost=0,
                flavor_text="화염 임프가 작은 불씨를 날렸다!",
            ),
            Action(
                name="화염탄",
                effects=[
                    DamageEffect(
                        power=0.9,
                        stat="magic",
                    ),
                    AddStatusEffect(
                        status_class=BurnStatus,
                        status_kwargs={
                            "power": 1,
                            "duration": 3,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="화염 임프가 뜨거운 화염탄을 쏘아냈다!",
            ),
            Action(
                name="불꽃 난사",
                effects=[
                    DamageEffect(
                        power=0.5,
                        stat="magic",
                    ),
                    AddStatusEffect(
                        status_class=BurnStatus,
                        status_kwargs={
                            "power": 1,
                            "duration": 3,
                        },
                    ),
                    DamageEffect(
                        power=0.5,
                        stat="magic",
                    ),
                    AddStatusEffect(
                        status_class=BurnStatus,
                        status_kwargs={
                            "power": 1,
                            "duration": 3,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="화염 임프가 연달아 불꽃을 퍼부었다!",
            ),
        ],
    ),

    Enemy(
        name="빙결 정령",
        max_hp=50,
        speed=10,
        attack=2,
        magic=6,
        defense=4,
        gold=50,
        action_pool=[
            Action(
                name="냉기탄",
                effects=[
                    DamageEffect(
                        power=0.7,
                        stat="magic",
                    ),
                    AddStatusEffect(
                        status_class=ColdStatus,
                        status_kwargs={
                            "stack": 2,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="빙결 정령이 차가운 냉기탄을 발사했다!",
            ),
            Action(
                name="얼음 장막",
                effects=[
                    BlockEffect(
                        power=1.3,
                        stat="magic",
                    ),
                ],
                mp_cost=0,
                flavor_text="빙결 정령이 얼음의 장막을 둘렀다!",
            ),
            Action(
                name="빙결창",
                effects=[
                    DamageEffect(
                        power=1.1,
                        stat="magic",
                    ),
                    AddStatusEffect(
                        status_class=ColdStatus,
                        status_kwargs={
                            "stack": 4,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="빙결 정령이 날카로운 얼음창을 쏘아냈다!",
            ),
        ],
    ),

    Enemy(
        name="피에 굶주린 광인",
        max_hp=52,
        speed=11,
        attack=5,
        defense=3,
        gold=50,
        action_pool=[
            Action(
                name="베기",
                effects=[
                    DamageEffect(
                        power=0.9,
                    ),
                    AddStatusEffect(
                        status_class=BleedStatus,
                        status_kwargs={
                            "stack": 1,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="광인이 웃으며 칼날을 휘둘렀다!",
            ),
            Action(
                name="난도질",
                effects=[
                    DamageEffect(
                        power=0.5,
                    ),
                    AddStatusEffect(
                        status_class=BleedStatus,
                        status_kwargs={
                            "stack": 1,
                        },
                    ),
                    DamageEffect(
                        power=0.5,
                    ),
                    AddStatusEffect(
                        status_class=BleedStatus,
                        status_kwargs={
                            "stack": 1,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="광인이 미친 듯이 칼을 휘둘렀다!",
            ),
            Action(
                name="처형",
                effects=[
                    DamageEffect(
                        power=1.8,
                    ),
                ],
                mp_cost=0,
                flavor_text="광인이 양손으로 무기를 치켜들고 내려찍었다!",
            ),
        ],
    ),

    Enemy(
        name="독성 슬라임",
        max_hp=62,
        speed=7,
        attack=5,
        defense=7,
        gold=50,
        action_pool=[
            Action(
                name="독성 몸통박치기",
                effects=[
                    DamageEffect(
                        power=1.2,
                    ),
                    AddStatusEffect(
                        status_class=PoisonStatus,
                        status_kwargs={
                            "stack": 2,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="독성 슬라임이 독액을 흩뿌리며 몸통박치기했다!",
            ),
            Action(
                name="독액",
                effects=[
                    AddStatusEffect(
                        status_class=PoisonStatus,
                        status_kwargs={
                            "stack": 4,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="독성 슬라임이 짙은 독액을 뿜어냈다!",
            ),
            Action(
                name="웅크리기",
                effects=[
                    BlockEffect(
                        power=1.5,
                    ),
                ],
                mp_cost=0,
                flavor_text="독성 슬라임이 몸을 단단하게 웅크렸다!",
            ),
        ],
    ),

    Enemy(
        name="화염 기사",
        max_hp=64,
        speed=9,
        attack=6,
        magic=4,
        defense=7,
        gold=55,
        action_pool=[
            Action(
                name="방패 올리기",
                effects=[
                    BlockEffect(
                        power=1.5,
                    ),
                ],
                mp_cost=0,
                flavor_text="화염 기사가 방패를 들어 자세를 굳혔다!",
            ),
            Action(
                name="화염 베기",
                effects=[
                    DamageEffect(
                        power=1.0,
                    ),
                    AddStatusEffect(
                        status_class=BurnStatus,
                        status_kwargs={
                            "power": 1,
                            "duration": 2,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="화염 기사의 검에서 불꽃이 솟구쳤다!",
            ),
            Action(
                name="강타",
                effects=[
                    DamageEffect(
                        power=2.0,
                    ),
                ],
                mp_cost=0,
                flavor_text="화염 기사가 불타는 검을 힘껏 내리쳤다!",
            ),
        ],
    ),

    Enemy(
        name="얼어붙은 갑옷",
        max_hp=78,
        speed=5,
        attack=7,
        defense=10,
        gold=60,
        action_pool=[
            Action(
                name="철벽",
                effects=[
                    BlockEffect(
                        power=1.5,
                    ),
                ],
                mp_cost=0,
                flavor_text="얼어붙은 갑옷이 묵묵히 방어 자세를 취했다!",
            ),
            Action(
                name="냉기 베기",
                effects=[
                    DamageEffect(
                        power=1.0,
                    ),
                    AddStatusEffect(
                        status_class=ColdStatus,
                        status_kwargs={
                            "stack": 3,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="서리 낀 검이 차가운 궤적을 그렸다!",
            ),
            Action(
                name="대검 강타",
                effects=[
                    DamageEffect(
                        power=2.5,
                    ),
                ],
                mp_cost=0,
                flavor_text="얼어붙은 갑옷이 무거운 대검을 내리쳤다!",
            ),
        ],
    ),

    Enemy(
        name="흡혈귀",
        max_hp=54,
        speed=13,
        attack=5,
        magic=5,
        defense=3,
        gold=60,
        action_pool=[
            Action(
                name="할퀴기",
                effects=[
                    DamageEffect(
                        power=0.8,
                    ),
                    AddStatusEffect(
                        status_class=BleedStatus,
                        status_kwargs={
                            "stack": 2,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="흡혈귀가 날카로운 손톱으로 상처를 냈다!",
            ),
            Action(
                name="흡혈",
                effects=[
                    DamageEffect(
                        power=0.8,
                    ),
                    RestoreHpEffect(
                        power=0.8,
                        stat="attack",
                    ),
                ],
                mp_cost=0,
                flavor_text="흡혈귀가 상처에서 흘러나온 피를 빨아들였다!",
            ),
            Action(
                name="피의 갈망",
                effects=[
                    DamageEffect(
                        power=1.3,
                    ),
                    RestoreHpEffect(
                        power=0.5,
                        stat="attack",
                    ),
                ],
                mp_cost=0,
                flavor_text="흡혈귀가 피에 굶주린 채 달려들었다!",
            ),
        ],
    ),

    Enemy(
        name="광신도 사제",
        max_hp=54,
        speed=8,
        attack=4,
        magic=6,
        defense=4,
        gold=55,
        action_pool=[
            Action(
                name="징벌",
                effects=[
                    DamageEffect(
                        power=0.9,
                        stat="magic",
                    ),
                ],
                mp_cost=0,
                flavor_text="광신도 사제가 저주 섞인 빛을 쏘아냈다!",
            ),
            Action(
                name="기도",
                effects=[
                    RestoreHpEffect(
                        power=1.0,
                        stat="magic",
                    ),
                ],
                mp_cost=0,
                flavor_text="광신도 사제가 기도하며 상처를 회복했다!",
            ),
            Action(
                name="신앙의 방벽",
                effects=[
                    BlockEffect(
                        power=1.3,
                        stat="magic",
                    ),
                ],
                mp_cost=0,
                flavor_text="광신도 사제가 기괴한 성구를 읊으며 방벽을 펼쳤다!",
            ),
        ],
    ),

    Enemy(
        name="폭탄 고블린",
        max_hp=45,
        speed=11,
        attack=4,
        defense=2,
        gold=55,
        action_pool=[
            Action(
                name="화약 준비",
                effects=[
                    BlockEffect(
                        power=0.8,
                    ),
                ],
                mp_cost=0,
                flavor_text="폭탄 고블린이 낄낄거리며 화약통을 꺼냈다!",
            ),
            Action(
                name="폭탄 투척",
                effects=[
                    DamageEffect(
                        power=1.5,
                    ),
                ],
                mp_cost=0,
                flavor_text="폭탄 고블린이 폭탄을 냅다 던졌다!",
            ),
            Action(
                name="화약 과충전",
                effects=[
                    BlockEffect(
                        power=0.5,
                    ),
                ],
                mp_cost=0,
                flavor_text="폭탄 고블린이 더 큰 폭탄에 불을 붙였다!",
            ),
            Action(
                name="대폭발",
                effects=[
                    DamageEffect(
                        power=3.0,
                    ),
                ],
                mp_cost=0,
                flavor_text="콰아아아앙!! 폭탄 고블린의 대폭발!",
            ),
        ],
    ),
]

enemies_third_floor_early = [
    [
        Enemy(
            name="중장 방패병",
            max_hp=115,
            speed=7,
            attack=5,
            defense=13,
            gold=45,
            action_pool=[
                Action(
                    name="엄호",
                    effects=[
                        BlockEffect(
                            power=1.5,
                            target_type="ally",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="중장 방패병이 아군의 앞을 가로막았다!",
                ),
                Action(
                    name="방패 치기",
                    effects=[
                        DamageEffect(power=1.0),
                        BlockEffect(
                            power=1.0,
                            target_type="ally",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="중장 방패병이 거대한 방패로 당신을 후려쳤다!",
                ),
                Action(
                    name="철벽 엄호",
                    effects=[
                        BlockEffect(
                            power=2.0,
                            target_type="ally",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="중장 방패병이 방패를 굳게 세워 아군을 보호했다!",
                ),
            ],
        ),
        Enemy(
            name="석궁병",
            max_hp=72,
            speed=13,
            attack=7,
            defense=3,
            gold=45,
            action_pool=[
                Action(
                    name="석궁 사격",
                    effects=[
                        DamageEffect(power=1.5),
                    ],
                    mp_cost=0,
                    flavor_text="석궁병이 당신을 향해 석궁을 발사했다!",
                ),
                Action(
                    name="견제 사격",
                    effects=[
                        DamageEffect(power=0.5),
                        DamageEffect(power=0.5),
                    ],
                    mp_cost=0,
                    flavor_text="석궁병이 움직임을 견제하듯 빠르게 화살을 날렸다!",
                ),
                Action(
                    name="조준 사격",
                    effects=[
                        DamageEffect(power=2.2),
                    ],
                    mp_cost=0,
                    flavor_text="석궁병이 침착하게 조준한 뒤 강력한 화살을 발사했다!",
                ),
            ],
        ),
    ],
    [
        Enemy(
            name="전투 주술사",
            max_hp=80,
            speed=10,
            attack=4,
            defense=4,
            gold=40,
            action_pool=[
                Action(
                    name="전투의 함성",
                    effects=[
                        AddStatusEffect(
                            status_class=StrengthenStatus,
                            status_kwargs={
                                "power": 0.25,
                                "duration": 3,
                            },
                            target_type="all_allies",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="전투 주술사가 아군의 사기를 끌어올렸다!",
                ),
                Action(
                    name="주술탄",
                    effects=[
                        DamageEffect(power=1.0),
                    ],
                    mp_cost=0,
                    flavor_text="전투 주술사가 기묘한 탄환을 날렸다!",
                ),
                Action(
                    name="가속의 주술",
                    effects=[
                        AddStatusEffect(
                            status_class=HasteStatus,
                            status_kwargs={
                                "power": 0,
                                "flat": 20,
                                "duration": 3,
                            },
                            target_type="all_allies",
                        ),
                        DamageEffect(power=0.7),
                    ],
                    mp_cost=0,
                    flavor_text="전투 주술사가 아군을 가속시켰다!",
                ),
            ],
        ),
        Enemy(
            name="돌격병",
            max_hp=90,
            speed=11,
            attack=8,
            defense=6,
            gold=40,
            action_pool=[
                Action(
                    name="돌진",
                    effects=[
                        DamageEffect(power=1.3),
                    ],
                    mp_cost=0,
                    flavor_text="돌격병이 거칠게 돌진해왔다!",
                ),
                Action(
                    name="휘두르기",
                    effects=[
                        DamageEffect(power=1.0),
                    ],
                    mp_cost=0,
                    flavor_text="돌격병이 무기를 크게 휘둘렀다!",
                ),
                Action(
                    name="맹렬한 돌격",
                    effects=[
                        DamageEffect(power=1.8),
                    ],
                    mp_cost=0,
                    flavor_text="돌격병이 전력을 다해 돌진했다!",
                ),
            ],
        ),
        Enemy(
            name="돌격병",
            max_hp=90,
            speed=11,
            attack=8,
            defense=6,
            gold=40,
            action_pool=[
                Action(
                    name="돌진",
                    effects=[
                        DamageEffect(power=1.3),
                    ],
                    mp_cost=0,
                    flavor_text="돌격병이 거칠게 돌진해왔다!",
                ),
                Action(
                    name="휘두르기",
                    effects=[
                        DamageEffect(power=1.0),
                    ],
                    mp_cost=0,
                    flavor_text="돌격병이 무기를 크게 휘둘렀다!",
                ),
                Action(
                    name="맹렬한 돌격",
                    effects=[
                        DamageEffect(power=1.8),
                    ],
                    mp_cost=0,
                    flavor_text="돌격병이 전력을 다해 당신에게 돌진했다!",
                ),
            ],
        ),
    ],
    [
        Enemy(
            name="전투 사제",
            max_hp=82,
            speed=9,
            attack=4,
            magic=8,
            defense=4,
            gold=40,
            action_pool=[
                Action(
                    name="치유",
                    effects=[
                        RestoreHpEffect(
                            power=1.5,
                            flat=8,
                            target_type="ally",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="전투 사제가 아군의 상처를 치유했다!",
                ),
                Action(
                    name="지팡이 타격",
                    effects=[
                        DamageEffect(power=1.0),
                    ],
                    mp_cost=0,
                    flavor_text="전투 사제가 지팡이를 휘둘렀다!",
                ),
                Action(
                    name="응급 광역 치유",
                    effects=[
                        RestoreHpEffect(
                            power=0.8,
                            flat=5,
                            target_type="all_allies",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="전투 사제가 짧은 기도로 아군의 상처를 봉합했다!",
                ),

            ],
        ),
        Enemy(
            name="중갑 검사",
            max_hp=105,
            speed=10,
            attack=8,
            defense=9,
            gold=50,
            action_pool=[
                Action(
                    name="베기",
                    effects=[
                        DamageEffect(power=1.3),
                    ],
                    mp_cost=0,
                    flavor_text="중갑 검사가 검을 크게 휘둘렀다!",
                ),
                Action(
                    name="방어 자세",
                    effects=[
                        BlockEffect(power=1.2),
                    ],
                    mp_cost=0,
                    flavor_text="중갑 검사가 검을 세우고 단단히 자세를 잡았다!",
                ),
                Action(
                    name="강하게 베기",
                    effects=[
                        DamageEffect(power=2.0),
                    ],
                    mp_cost=0,
                    flavor_text="중갑 검사가 체중을 실어 검을 힘껏 내리쳤다!",
                ),
            ],
        ),
    ],
]

enemies_third_floor = [
    [
        Enemy(
            name="냉기술사",
            max_hp=78,
            speed=12,
            attack=5,
            magic=7,
            defense=5,
            gold=55,
            action_pool=[
                Action(
                    name="서리탄",
                    effects=[
                        DamageEffect(
                            power=0.8,
                            stat="magic",
                        ),
                        AddStatusEffect(
                            status_class=ColdStatus,
                            status_kwargs={
                                "stack": 4,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="냉기술사가 차가운 마력탄을 날렸다!",
                ),
                Action(
                    name="혹한의 바람",
                    effects=[
                        AddStatusEffect(
                            status_class=ColdStatus,
                            status_kwargs={
                                "stack": 5,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="냉기술사가 얼어붙는 바람을 일으켰다!",
                ),
                Action(
                    name="얼음 화살",
                    effects=[
                        DamageEffect(
                            power=1.2,
                            stat="magic",
                        ),
                        AddStatusEffect(
                            status_class=ColdStatus,
                            status_kwargs={
                                "stack": 3,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="냉기술사가 날카로운 얼음 화살을 쏘아냈다!",
                ),
            ],
        ),
        Enemy(
            name="처형자",
            max_hp=120,
            speed=8,
            attack=10,
            defense=8,
            gold=65,
            action_pool=[
                Action(
                    name="횡베기",
                    effects=[
                        DamageEffect(
                            power=1.2,
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="처형자가 거대한 무기를 옆으로 휘둘렀다!",
                ),
                Action(
                    name="내려찍기",
                    effects=[
                        DamageEffect(
                            power=1.6,
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="처형자가 무기를 힘껏 내려찍었다!",
                ),
                Action(
                    name="처형",
                    effects=[
                        DamageEffect(
                            power=3.0,
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="처형자가 온 힘을 실어 치명적인 일격을 내리쳤다!",
                ),
            ],
        ),
    ],
    [
        Enemy(
            name="독술사",
            max_hp=80,
            speed=9,
            attack=4,
            magic=7,
            defense=5,
            gold=60,
            action_pool=[
                Action(
                    name="독침",
                    effects=[
                        DamageEffect(
                            power=0.8,
                            stat="magic",
                        ),
                        AddStatusEffect(
                            status_class=PoisonStatus,
                            status_kwargs={
                                "stack": 2,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="독술사가 독이 묻은 침을 날렸다!",
                ),
                Action(
                    name="맹독 폭발",
                    effects=[
                        PoisonBurstEffect(),
                    ],
                    mp_cost=0,
                    flavor_text="독술사가 몸속에 쌓인 독을 강제로 폭발시켰다!",
                ),
                Action(
                    name="맹독 증폭",
                    effects=[
                        MultiplyPoisonEffect(
                            power=1.5,
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="독술사가 몸속의 독을 증폭시켰다!",
                ),
            ],
        ),
        Enemy(
            name="맹독충",
            max_hp=62,
            speed=13,
            attack=6,
            defense=4,
            gold=40,
            action_pool=[
                Action(
                    name="독니",
                    effects=[
                        DamageEffect(power=1.0),
                        AddStatusEffect(
                            status_class=PoisonStatus,
                            status_kwargs={
                                "stack": 3,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="맹독충이 독니를 박아넣었다!",
                ),
                Action(
                    name="맹독 분사",
                    effects=[
                        AddStatusEffect(
                            status_class=PoisonStatus,
                            status_kwargs={
                                "stack": 5,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="맹독충이 짙은 독액을 뿜어냈다!",
                ),
            ],
        ),
        Enemy(
            name="맹독충",
            max_hp=62,
            speed=13,
            attack=6,
            defense=4,
            gold=40,
            action_pool=[
                Action(
                    name="독니",
                    effects=[
                        DamageEffect(power=1.0),
                        AddStatusEffect(
                            status_class=PoisonStatus,
                            status_kwargs={
                                "stack": 3,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="맹독충이 독니를 박아넣었다!",
                ),
                Action(
                    name="맹독 분사",
                    effects=[
                        AddStatusEffect(
                            status_class=PoisonStatus,
                            status_kwargs={
                                "stack": 5,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="맹독충이 짙은 독액을 뿜어냈다!",
                ),
            ],
        ),
    ],
    [
        Enemy(
            name="전투 지휘관",
            max_hp=88,
            speed=10,
            attack=5,
            defense=7,
            gold=60,
            action_pool=[
                Action(
                    name="진격 명령",
                    effects=[
                        ActionGaugeEffect(
                            power=0,
                            flat=50,
                            target_type="all_allies",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="전투 지휘관이 아군에게 진격을 명령했다!",
                ),
                Action(
                    name="공격 명령",
                    effects=[
                        AddStatusEffect(
                            status_class=StrengthenStatus,
                            status_kwargs={
                                "power": 0.2,
                                "duration": 3,
                            },
                            target_type="all_allies",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="전투 지휘관의 명령에 적들의 공세가 거세졌다!",
                ),
                Action(
                    name="지휘검",
                    effects=[
                        DamageEffect(power=1.2),
                    ],
                    mp_cost=0,
                    flavor_text="전투 지휘관이 직접 검을 휘둘렀다!",
                ),
            ],
        ),
        Enemy(
            name="중장 방패병",
            max_hp=115,
            speed=7,
            attack=5,
            defense=13,
            gold=45,
            action_pool=[
                Action(
                    name="엄호",
                    effects=[
                        BlockEffect(
                            power=1.5,
                            target_type="ally",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="중장 방패병이 아군의 앞을 가로막았다!",
                ),
                Action(
                    name="방패 치기",
                    effects=[
                        DamageEffect(power=1.0),
                        BlockEffect(
                            power=1.0,
                            target_type="ally",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="중장 방패병이 거대한 방패로 당신을 후려쳤다!",
                ),
                Action(
                    name="철벽 엄호",
                    effects=[
                        BlockEffect(
                            power=2.0,
                            target_type="ally",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="중장 방패병이 방패를 굳게 세워 아군을 보호했다!",
                ),
            ],
        ),
        Enemy(
            name="석궁병",
            max_hp=72,
            speed=13,
            attack=7,
            defense=3,
            gold=45,
            action_pool=[
                Action(
                    name="석궁 사격",
                    effects=[
                        DamageEffect(power=1.5),
                    ],
                    mp_cost=0,
                    flavor_text="석궁병이 당신을 향해 석궁을 발사했다!",
                ),
                Action(
                    name="견제 사격",
                    effects=[
                        DamageEffect(power=0.5),
                        DamageEffect(power=0.5),
                    ],
                    mp_cost=0,
                    flavor_text="석궁병이 움직임을 견제하듯 빠르게 화살을 날렸다!",
                ),
                Action(
                    name="조준 사격",
                    effects=[
                        DamageEffect(power=2.2),
                    ],
                    mp_cost=0,
                    flavor_text="석궁병이 침착하게 조준한 뒤 강력한 화살을 발사했다!",
                ),
            ],
        ),
    ],
    [
        Enemy(
            name="흡혈 검사",
            max_hp=100,
            speed=11,
            attack=8,
            defense=6,
            gold=60,
            action_pool=[
                Action(
                    name="피의 참격",
                    effects=[
                        DamageEffect(power=1.3),
                        AddStatusEffect(
                            status_class=BleedStatus,
                            status_kwargs={
                                "stack": 3,
                            },
                        ),
                        RestoreHpEffect(
                            power=0.5,
                            target_type="self",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="흡혈 검사가 피를 갈구하며 검을 휘둘렀다!",
                ),
                Action(
                    name="흡혈",
                    effects=[
                        DamageEffect(power=1.6),
                        AddStatusEffect(
                            status_class=BleedStatus,
                            status_kwargs={
                                "stack": 3,
                            },
                        ),
                        RestoreHpEffect(
                            power=0.8,
                            target_type="self",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="흡혈 검사가 상처에서 흘러나온 피를 빨아들였다!",
                ),
                Action(
                    name="난도질",
                    effects=[
                        DamageEffect(power=0.3),
                        AddStatusEffect(
                            status_class=BleedStatus,
                            status_kwargs={
                                "stack": 2,
                            },
                        ),
                       DamageEffect(power=0.3),
                        AddStatusEffect(
                            status_class=BleedStatus,
                            status_kwargs={
                                "stack": 2,
                            },
                        ),
                       DamageEffect(power=0.3),
                        AddStatusEffect(
                            status_class=BleedStatus,
                            status_kwargs={
                                "stack": 2,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="흡혈 검사가 상처를 깊게 벌리듯 연달아 베어냈다!",
                ),
            ],
        ),
        Enemy(
            name="전투 사제",
            max_hp=82,
            speed=9,
            attack=4,
            defense=4,
            gold=40,
            action_pool=[
                Action(
                    name="치유",
                    effects=[
                        RestoreHpEffect(
                            power=1.5,
                            flat=8,
                            target_type="ally",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="전투 사제가 아군의 상처를 치유했다!",
                ),
                Action(
                    name="지팡이 타격",
                    effects=[
                        DamageEffect(power=1.0),
                    ],
                    mp_cost=0,
                    flavor_text="전투 사제가 지팡이를 휘둘렀다!",
                ),
                Action(
                    name="응급 광역 치유",
                    effects=[
                        RestoreHpEffect(
                            power=0.8,
                            flat=5,
                            target_type="all_allies",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="전투 사제가 짧은 기도로 아군의 상처를 봉합했다!",
                ),

            ],
        ),
    ],
    [
        Enemy(
            name="불씨 정령",
            max_hp=62,
            speed=14,
            attack=3,
            magic=6,
            defense=3,
            gold=45,
            action_pool=[
                Action(
                    name="불씨 날리기",
                    effects=[
                        DamageEffect(
                            power=0.6,
                            stat="magic",
                        ),
                        AddStatusEffect(
                            status_class=BurnStatus,
                            status_kwargs={
                                "power": 1,
                                "duration": 4,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="불씨 정령이 꺼지지 않는 작은 불씨를 날렸다!",
                ),
                Action(
                    name="불꽃 몸통박치기",
                    effects=[
                        DamageEffect(
                            power=0.9,
                            stat="magic",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="불씨 정령이 불꽃을 흩뿌리며 달려들었다!",
                ),
                Action(
                    name="잔불",
                    effects=[
                        AddStatusEffect(
                            status_class=BurnStatus,
                            status_kwargs={
                                "power": 1,
                                "duration": 4,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="꺼져가던 불씨가 다시 거세게 타올랐다!",
                ),
            ],
        ),
        Enemy(
            name="화염술사",
            max_hp=80,
            speed=11,
            attack=4,
            magic=7,
            defense=4,
            gold=55,
            action_pool=[
                Action(
                    name="화염탄",
                    effects=[
                        DamageEffect(
                            power=1.0,
                            stat="magic",
                        ),
                        AddStatusEffect(
                            status_class=BurnStatus,
                            status_kwargs={
                                "power": 3,
                                "duration": 1,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="화염술사가 응축된 화염탄을 쏘아냈다!",
                ),
                Action(
                    name="불꽃 파동",
                    effects=[
                        DamageEffect(
                            power=0.8,
                            stat="magic",
                        ),
                        AddStatusEffect(
                            status_class=BurnStatus,
                            status_kwargs={
                                "power": 3,
                                "duration": 1,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="화염술사가 뜨거운 불꽃을 폭발시키듯 퍼뜨렸다!",
                ),
                Action(
                    name="화염창",
                    effects=[
                        DamageEffect(
                            power=1.5,
                            stat="magic",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="화염술사가 날카로운 화염창을 쏘아냈다!",
                ),
            ],
        ),
        Enemy(
            name="작열 기사",
            max_hp=80,
            speed=9,
            attack=8,
            magic=5,
            defense=9,
            gold=65,
            action_pool=[
                Action(
                    name="작열 베기",
                    effects=[
                        DamageEffect(
                            power=1.2,
                        ),
                        AddStatusEffect(
                            status_class=BurnStatus,
                            status_kwargs={
                                "power": 2,
                                "duration": 2,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="화염 기사가 불타는 검을 휘둘렀다!",
                ),
                Action(
                    name="방패 올리기",
                    effects=[
                        BlockEffect(
                            power=1.5,
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="화염 기사가 방패를 들어 공격에 대비했다!",
                ),
                Action(
                    name="불꽃 내려찍기",
                    effects=[
                        DamageEffect(
                            power=1.6,
                        ),
                        AddStatusEffect(
                            status_class=BurnStatus,
                            status_kwargs={
                                "power": 2,
                                "duration": 2,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="화염 기사가 불타는 검을 힘껏 내려찍었다!",
                ),
            ],
        ),
    ],
    [
        Enemy(
            name="중갑 검사",
            max_hp=105,
            speed=10,
            attack=8,
            defense=9,
            gold=50,
            action_pool=[
                Action(
                    name="베기",
                    effects=[
                        DamageEffect(power=1.3),
                    ],
                    mp_cost=0,
                    flavor_text="중갑 검사가 검을 크게 휘둘렀다!",
                ),
                Action(
                    name="방어 자세",
                    effects=[
                        BlockEffect(power=1.2),
                    ],
                    mp_cost=0,
                    flavor_text="중갑 검사가 검을 세우고 단단히 자세를 잡았다!",
                ),
                Action(
                    name="강하게 베기",
                    effects=[
                        DamageEffect(power=2.0),
                    ],
                    mp_cost=0,
                    flavor_text="중갑 검사가 체중을 실어 검을 힘껏 내리쳤다!",
                ),
            ],
        ),
        Enemy(
            name="돌격병",
            max_hp=90,
            speed=11,
            attack=8,
            defense=6,
            gold=40,
            action_pool=[
                Action(
                    name="돌진",
                    effects=[
                        DamageEffect(power=1.3),
                    ],
                    mp_cost=0,
                    flavor_text="돌격병이 거칠게 돌진해왔다!",
                ),
                Action(
                    name="휘두르기",
                    effects=[
                        DamageEffect(power=1.0),
                    ],
                    mp_cost=0,
                    flavor_text="돌격병이 무기를 크게 휘둘렀다!",
                ),
                Action(
                    name="맹렬한 돌격",
                    effects=[
                        DamageEffect(power=1.8),
                    ],
                    mp_cost=0,
                    flavor_text="돌격병이 전력을 다해 당신에게 돌진했다!",
                ),
            ],
        ),
        Enemy(
            name="저주술사",
            max_hp=80,
            speed=10,
            attack=4,
            magic=6,
            defense=4,
            gold=60,
            action_pool=[
                Action(
                    name="쇠약의 저주",
                    effects=[
                        AddStatusEffect(
                            status_class=WeakenStatus,
                            status_kwargs={
                                "power": 0.2,
                                "duration": 3,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="저주술사가 힘을 빼앗는 저주를 걸었다!",
                ),
                Action(
                    name="무력화의 저주",
                    effects=[
                        AddStatusEffect(
                            status_class=EnfeebleStatus,
                            status_kwargs={
                                "power": 0.2,
                                "duration": 3,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="저주술사가 몸을 무겁게 만드는 저주를 걸었다!",
                ),
                Action(
                    name="파멸의 저주",
                    effects=[
                        AddStatusEffect(
                            status_class=VulnerableStatus,
                            status_kwargs={
                                "power": 0.25,
                                "duration": 3,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="저주술사가 방어의 빈틈을 드러내는 저주를 걸었다!",
                ),
            ],
        ),
    ],
    [
        Enemy(
            name="결투가",
            max_hp=95,
            speed=12,
            attack=8,
            defense=6,
            gold=60,
            action_pool=[
                Action(
                    name="견제",
                    effects=[
                        DamageEffect(power=1.0),
                    ],
                    mp_cost=0,
                    flavor_text="결투가가 거리를 재며 빠르게 검을 휘둘렀다!",
                ),
                Action(
                    name="반격 자세",
                    effects=[
                        AddStatusEffect(
                            status_class=CounterStatus,
                            status_kwargs={
                                "power": 1.5,
                            },
                            target_type="self",
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="결투가가 검을 세우고 당신의 공격을 기다린다!",
                ),
                Action(
                    name="일섬",
                    effects=[
                        DamageEffect(power=1.8),
                    ],
                    mp_cost=0,
                    flavor_text="결투가가 빈틈을 노려 날카롭게 검을 그었다!",
                ),
            ],
        ),
        Enemy(
            name="석궁병",
            max_hp=72,
            speed=13,
            attack=7,
            defense=3,
            gold=45,
            action_pool=[
                Action(
                    name="석궁 사격",
                    effects=[
                        DamageEffect(power=1.5),
                    ],
                    mp_cost=0,
                    flavor_text="석궁병이 당신을 향해 석궁을 발사했다!",
                ),
                Action(
                    name="견제 사격",
                    effects=[
                        DamageEffect(power=0.5),
                        DamageEffect(power=0.5),
                    ],
                    mp_cost=0,
                    flavor_text="석궁병이 움직임을 견제하듯 빠르게 화살을 날렸다!",
                ),
                Action(
                    name="조준 사격",
                    effects=[
                        DamageEffect(power=2.2),
                    ],
                    mp_cost=0,
                    flavor_text="석궁병이 침착하게 조준한 뒤 강력한 화살을 발사했다!",
                ),
            ],
        ),
    ],
]

commander_phase_1 = [
    Action(
        name="진격 명령",
        effects=[
            ActionGaugeEffect(
                flat=30,
                target_type="all_allies",
            ),
        ],
        flavor_text="전장 지휘관이 아군에게 진격을 명령했다!",
    ),
    Action(
        name="공격 명령",
        effects=[
            AddStatusEffect(
                status_class=StrengthenStatus,
                status_kwargs={
                    "power": 0.2,
                    "duration": 3,
                },
                target_type="all_allies",
            ),
        ],
        flavor_text="전장 지휘관이 전군에 공격을 명령했다!",
    ),
    Action(
        name="지휘검",
        effects=[
            DamageEffect(power=1.2),
        ],
        flavor_text="전장 지휘관이 검을 휘둘렀다!",
    ),
]
commander_phase_2 = [
    Action(
        name="전열 재정비",
        effects=[
            BlockEffect(
                power=1.5,
                target_type="all_allies",
            ),
        ],
        mp_cost=0,
        flavor_text="전장 지휘관이 무너진 전열을 빠르게 재정비했다!",
    ),
    Action(
        name="돌격 명령",
        effects=[
            ActionGaugeEffect(
                power=0,
                flat=50,
                target_type="all_allies",
            ),
            AddStatusEffect(
                status_class=StrengthenStatus,
                status_kwargs={
                    "power": 0.15,
                    "duration": 2,
                },
                target_type="all_allies",
            ),
        ],
        mp_cost=0,
        flavor_text="전장 지휘관이 남은 병력에게 전면 돌격을 명령했다!",
    ),
    Action(
        name="강습",
        effects=[
            DamageEffect(power=1.8),
        ],
        mp_cost=0,
        flavor_text="전장 지휘관이 직접 전열을 돌파하며 공격했다!",
    ),
]
commander_phase_3 = [
    Action(
        name="결사항전",
        effects=[
            AddStatusEffect(
                status_class=StrengthenStatus,
                status_kwargs={
                    "power": 0.3,
                    "duration": 3,
                },
                target_type="self",
            ),
        ],
        mp_cost=0,
        flavor_text="전장 지휘관이 남은 힘을 모두 끌어올렸다!",
    ),
    Action(
        name="연속 참격",
        effects=[
            DamageEffect(
                power=0.9,
            ),
            DamageEffect(
                power=0.9,
            ),
        ],
        mp_cost=0,
        flavor_text="전장 지휘관이 숨 돌릴 틈 없이 연속으로 검을 휘둘렀다!",
    ),
    Action(
        name="최후의 돌격",
        effects=[
            DamageEffect(power=2.5),
        ],
        mp_cost=0,
        flavor_text="전장 지휘관이 모든 것을 건 최후의 돌격을 감행했다!",
    ),
]

bosses = [
    Enemy(
        name="거대 슬라임",
        max_hp=150,
        speed=6,
        attack=10,
        defense=10,
        gold=50,
        action_pool=[
            Action(
                name="더블 배럴 샷건",
                effects=[DamageEffect(power=1.5), DamageEffect(power=1.5)],
                mp_cost=0,
                flavor_text="거대 슬라임이 당신에게 더블 배럴 샷건을 쐈다!!",
            ),
            Action(
                name="웅크리기",
                effects=[BlockEffect(power=2)],
                mp_cost=0,
                flavor_text="거대 슬라임은 몸을 웅크린다!",
            ),
            Action(
                name="공격",
                effects=[DamageEffect()],
                mp_cost=0,
                flavor_text="거대 슬라임은 당신을 공격했다!",
            ),
        ],
    ),
    Enemy(
        name="융합 마도 골렘",
        max_hp=400,
        speed=7,
        attack=7,
        magic=8,
        defense=10,
        gold=120,
        action_pool=[
            Action(
                name="독성 증기",
                effects=[
                    AddStatusEffect(
                        status_class=PoisonStatus,
                        status_kwargs={
                            "stack": 4,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="융합 마도 골렘의 몸에서 짙은 독성 증기가 뿜어져 나왔다!",
            ),
            Action(
                name="화염 방사",
                effects=[
                    DamageEffect(
                        power=1.0,
                        stat="magic",
                    ),
                    AddStatusEffect(
                        status_class=BurnStatus,
                        status_kwargs={
                            "power": 3,
                            "duration": 4,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="융합 마도 골렘이 전방으로 거대한 화염을 뿜었다!",
            ),
            Action(
                name="냉각 장치 가동",
                effects=[
                    BlockEffect(
                        power=1.5,
                        stat="defense",
                    ),
                    AddStatusEffect(
                        status_class=ColdStatus,
                        status_kwargs={
                            "stack": 9,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="융합 마도 골렘이 장갑을 냉각하며 주변의 열기를 빼앗았다!",
            ),
            Action(
                name="회전 톱날",
                effects=[
                    DamageEffect(
                        power=0.6,
                        stat="attack",
                    ),
                    AddStatusEffect(
                        status_class=BleedStatus,
                        status_kwargs={
                            "stack": 4,
                        },
                    ),
                    DamageEffect(
                        power=0.6,
                        stat="attack",
                    ),
                    AddStatusEffect(
                        status_class=BleedStatus,
                        status_kwargs={
                            "stack": 4,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="융합 마도 골렘의 양팔에서 회전 톱날이 튀어나왔다!",
            ),
            Action(
                name="마력 과부하",
                effects=[
                    DamageEffect(
                        power=2.2,
                        stat="magic",
                    ),
                ],
                mp_cost=0,
                flavor_text="경고음이 울린다! 융합 마도 골렘이 축적한 마력을 폭발시켰다!",
            ),
        ],
    ),
    [
        Enemy(
            name="처형자",
            max_hp=120,
            speed=8,
            attack=10,
            defense=8,
            gold=65,
            action_pool=[
                Action(
                    name="횡베기",
                    effects=[
                        DamageEffect(
                            power=1.2,
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="처형자가 거대한 무기를 옆으로 휘둘렀다!",
                ),
                Action(
                    name="내려찍기",
                    effects=[
                        DamageEffect(
                            power=1.6,
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="처형자가 무기를 힘껏 내려찍었다!",
                ),
                Action(
                    name="처형",
                    effects=[
                        DamageEffect(
                            power=3.0,
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="처형자가 온 힘을 실어 치명적인 일격을 내리쳤다!",
                ),
            ],
        ),
        Enemy(
            name="전장 지휘관",
            max_hp=360,
            speed=12,
            attack=9,
            magic=8,
            defense=10,
            gold=150,
            action_pool=commander_phase_1,
            action_pools={
                2: commander_phase_1,
                1: commander_phase_2,
                0: commander_phase_3,
            },
        ),
        Enemy(
            name="저주술사",
            max_hp=80,
            speed=10,
            attack=4,
            magic=6,
            defense=4,
            gold=60,
            action_pool=[
                Action(
                    name="쇠약의 저주",
                    effects=[
                        AddStatusEffect(
                            status_class=WeakenStatus,
                            status_kwargs={
                                "power": 0.2,
                                "duration": 3,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="저주술사가 힘을 빼앗는 저주를 걸었다!",
                ),
                Action(
                    name="무력화의 저주",
                    effects=[
                        AddStatusEffect(
                            status_class=EnfeebleStatus,
                            status_kwargs={
                                "power": 0.2,
                                "duration": 3,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="저주술사가 몸을 무겁게 만드는 저주를 걸었다!",
                ),
                Action(
                    name="파멸의 저주",
                    effects=[
                        AddStatusEffect(
                            status_class=VulnerableStatus,
                            status_kwargs={
                                "power": 0.25,
                                "duration": 3,
                            },
                        ),
                    ],
                    mp_cost=0,
                    flavor_text="저주술사가 방어의 빈틈을 드러내는 저주를 걸었다!",
                ),
            ],
        ),
    ],
]

four_kings = [
    Enemy(
        name="사천왕-성직자",
        max_hp=260,
        speed=8,
        attack=6,
        magic=10,
        defense=6,
        gold=0,
        action_pool=[
            Action(
                name="빛",
                effects=[
                    DamageEffect(
                        power=0.7,
                        stat="magic",
                    ),
                    AddStatusEffect(
                        status_class=BurnStatus,
                        status_kwargs={
                            "power": 2,
                            "duration": 3,
                        },
                    ),
                    AddStatusEffect(
                        status_class=WeakenStatus,
                        status_kwargs={
                            "power": 0.2,
                            "duration": 2,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-성직자가 타오르는 빛을 내리쬐었다!",
            ),

            Action(
                name="축복",
                effects=[
                    AddStatusEffect(
                        status_class=StrengthenStatus,
                        status_kwargs={
                            "power": 0.2,
                            "duration": 2,
                        },
                        target_type="all_allies",
                    ),
                    ActionGaugeEffect(
                        power=0,
                        flat=40,
                        target_type="all_allies",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-성직자가 축복을 내렸다!",
            ),

            Action(
                name="기도",
                effects=[
                    BlockEffect(
                        power=0.8,
                        stat="magic",
                        target_type="all_allies",
                    ),
                    AddStatusEffect(
                        status_class=FortifyStatus,
                        status_kwargs={
                            "power": 0.5,
                            "flat": 2,
                            "stat": "defense",
                            "duration": 3,
                        },
                        target_type="all_allies",
                    ),
                    AddStatusEffect(
                        status_class=RegenerationStatus,
                        status_kwargs={
                            "power": 0,
                            "flat": 3,
                            "duration": 3,
                        },
                        target_type="all_allies",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-성직자가 경건한 기도를 올렸다!",
            ),

            Action(
                name="심판",
                effects=[
                    DamageEffect(
                        power=1.8,
                        stat="magic",
                        dice_count=1,
                        dice_sides=6,
                    ),
                    AddStatusEffect(
                        status_class=BurnStatus,
                        status_kwargs={
                            "power": 3,
                            "duration": 3,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-성직자가 신성한 불꽃으로 심판을 내렸다!",
            ),

            Action(
                name="축복",
                effects=[
                    AddStatusEffect(
                        status_class=StrengthenStatus,
                        status_kwargs={
                            "power": 0.2,
                            "duration": 2,
                        },
                        target_type="all_allies",
                    ),
                    ActionGaugeEffect(
                        power=0,
                        flat=40,
                        target_type="all_allies",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-성직자가 축복을 내렸다!",
            ),

            Action(
                name="기도",
                effects=[
                    BlockEffect(
                        power=0.8,
                        stat="magic",
                        target_type="all_allies",
                    ),
                    AddStatusEffect(
                        status_class=FortifyStatus,
                        status_kwargs={
                            "power": 0.5,
                            "flat": 2,
                            "stat": "defense",
                            "duration": 3,
                        },
                        target_type="all_allies",
                    ),
                    AddStatusEffect(
                        status_class=RegenerationStatus,
                        status_kwargs={
                            "power": 0,
                            "flat": 3,
                            "duration": 3,
                        },
                        target_type="all_allies",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-성직자가 경건한 기도를 올렸다!",
            ),
        ],
    ),
    Enemy(
        name="사천왕-기사",
        max_hp=320,
        speed=7,
        attack=11,
        magic=4,
        defense=12,
        gold=0,
        action_pool=[
            Action(
                name="수호",
                effects=[
                    BlockEffect(
                        power=1.3,
                        stat="defense",
                        flat=3,
                        target_type="all_allies",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-기사가 거대한 방패를 치켜들었다!",
            ),

            Action(
                name="일격",
                effects=[
                    DamageEffect(
                        power=1.0,
                        stat="attack",
                        dice_count=1,
                        dice_sides=6,
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-기사가 묵직하게 무기를 휘둘렀다!",
            ),

            Action(
                name="철벽",
                effects=[
                    BlockEffect(
                        power=1.8,
                        stat="defense",
                        flat=5,
                        target_type="self",
                    ),
                    AddStatusEffect(
                        status_class=CounterStatus,
                        status_kwargs={
                            "power": 1.2,
                            "flat": 0,
                            "dice_count": 1,
                            "dice_sides": 6,
                            "stat": "attack",
                        },
                        target_type="self",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-기사가 철벽의 자세를 취했다!",
            ),

            Action(
                name="분쇄",
                effects=[
                    DamageEffect(
                        power=1.8,
                        stat="attack",
                        dice_count=2,
                        dice_sides=6,
                    ),
                    AddStatusEffect(
                        status_class=VulnerableStatus,
                        status_kwargs={
                            "power": 0.25,
                            "duration": 2,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-기사가 무기를 힘껏 내리꽂았다!",
            ),

            Action(
                name="일격",
                effects=[
                    DamageEffect(
                        power=1.0,
                        stat="attack",
                        dice_count=1,
                        dice_sides=6,
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-기사가 묵직하게 무기를 휘둘렀다!",
            ),

            Action(
                name="철벽",
                effects=[
                    BlockEffect(
                        power=1.8,
                        stat="defense",
                        flat=5,
                        target_type="self",
                    ),
                    AddStatusEffect(
                        status_class=CounterStatus,
                        status_kwargs={
                            "power": 1.2,
                            "flat": 0,
                            "dice_count": 1,
                            "dice_sides": 6,
                            "stat": "attack",
                        },
                        target_type="self",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-기사가 철벽의 자세를 취했다!",
            ),
        ],
    ),
    Enemy(
        name="사천왕-마법사",
        max_hp=250,
        speed=9,
        attack=4,
        magic=11,
        defense=5,
        gold=0,
        action_pool=[
            Action(
                name="혹한",
                effects=[
                    DamageEffect(
                        power=0.8,
                        stat="magic",
                        dice_count=1,
                        dice_sides=4,
                    ),
                    AddStatusEffect(
                        status_class=ColdStatus,
                        status_kwargs={
                            "stack": 3,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-마법사가 얼어붙는 냉기를 쏟아냈다!",
            ),

            Action(
                name="화염구 연타",
                effects=[
                    DamageEffect(
                        power=0.45,
                        stat="magic",
                        dice_count=1,
                        dice_sides=4,
                    ),
                    DamageEffect(
                        power=0.45,
                        stat="magic",
                        dice_count=1,
                        dice_sides=4,
                    ),
                    DamageEffect(
                        power=0.45,
                        stat="magic",
                        dice_count=1,
                        dice_sides=4,
                    ),
                    AddStatusEffect(
                        status_class=BurnStatus,
                        status_kwargs={
                            "power": 3,
                            "duration": 3,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-마법사가 연달아 화염구를 내던졌다!",
            ),

            Action(
                name="저주",
                effects=[
                    AddStatusEffect(
                        status_class=WeakenStatus,
                        status_kwargs={
                            "power": 0.2,
                            "duration": 3,
                        },
                    ),
                    AddStatusEffect(
                        status_class=EnfeebleStatus,
                        status_kwargs={
                            "power": 0.2,
                            "duration": 3,
                        },
                    ),
                    AddStatusEffect(
                        status_class=PoisonStatus,
                        status_kwargs={
                            "stack": 4,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-마법사가 불길한 저주를 걸었다!",
            ),

            Action(
                name="마력탄",
                effects=[
                    DamageEffect(
                        power=0.35,
                        stat="magic",
                        dice_count=1,
                        dice_sides=3,
                    ),
                    DamageEffect(
                        power=0.35,
                        stat="magic",
                        dice_count=1,
                        dice_sides=3,
                    ),
                    DamageEffect(
                        power=0.35,
                        stat="magic",
                        dice_count=1,
                        dice_sides=3,
                    ),
                    DamageEffect(
                        power=0.35,
                        stat="magic",
                        dice_count=1,
                        dice_sides=3,
                    ),
                    DamageEffect(
                        power=0.35,
                        stat="magic",
                        dice_count=1,
                        dice_sides=3,
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-마법사가 수많은 마력탄을 퍼부었다!",
            ),

            Action(
                name="마력 집중",
                effects=[
                    AddStatusEffect(
                        status_class=StrengthenStatus,
                        status_kwargs={
                            "power": 0.5,
                            "duration": 2,
                        },
                        target_type="self",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-마법사가 막대한 마력을 끌어모으기 시작했다!",
            ),

            Action(
                name="대마법",
                effects=[
                    DamageEffect(
                        power=2.4,
                        stat="magic",
                        dice_count=3,
                        dice_sides=8,
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-마법사가 응축된 마력을 한꺼번에 폭발시켰다!",
            ),
        ],
    ),
    Enemy(
        name="사천왕-도적",
        max_hp=240,
        speed=13,
        attack=10,
        magic=4,
        defense=5,
        gold=0,
        action_pool=[
            Action(
                name="기습",
                effects=[
                    DamageEffect(
                        power=0.8,
                        stat="attack",
                        dice_count=1,
                        dice_sides=4,
                    ),
                    AddStatusEffect(
                        status_class=BleedStatus,
                        status_kwargs={
                            "stack": 2,
                        },
                    ),
                    ActionGaugeEffect(
                        power=0,
                        flat=25,
                        target_type="self",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-도적이 빈틈을 노려 기습했다!",
            ),

            Action(
                name="난도질",
                effects=[
                    DamageEffect(
                        power=0.45,
                        stat="attack",
                        dice_count=1,
                        dice_sides=3,
                    ),
                    DamageEffect(
                        power=0.45,
                        stat="attack",
                        dice_count=1,
                        dice_sides=3,
                    ),
                    DamageEffect(
                        power=0.45,
                        stat="attack",
                        dice_count=1,
                        dice_sides=3,
                    ),
                    AddStatusEffect(
                        status_class=BleedStatus,
                        status_kwargs={
                            "stack": 3,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-도적이 빠르게 칼날을 휘둘렀다!",
            ),

            Action(
                name="발목 베기",
                effects=[
                    DamageEffect(
                        power=0.8,
                        stat="attack",
                        dice_count=1,
                        dice_sides=4,
                    ),
                    ActionGaugeEffect(
                        power=0,
                        flat=-50,
                        target_type="enemy",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-도적이 낮게 파고들어 발목을 베었다!",
            ),

            Action(
                name="연막",
                effects=[
                    AddStatusEffect(
                        status_class=WeakenStatus,
                        status_kwargs={
                            "power": 0.2,
                            "duration": 2,
                        },
                    ),
                    AddStatusEffect(
                        status_class=DodgeStatus,
                        status_kwargs={
                            "count": 2,
                        },
                        target_type="self",
                    ),
                    ActionGaugeEffect(
                        power=0,
                        flat=75,
                        target_type="self",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-도적이 연막 속으로 모습을 감췄다!",
            ),

            Action(
                name="급소 찌르기",
                effects=[
                    DamageEffect(
                        power=1.7,
                        stat="attack",
                        dice_count=2,
                        dice_sides=6,
                    ),
                    AddStatusEffect(
                        status_class=VulnerableStatus,
                        status_kwargs={
                            "power": 0.25,
                            "duration": 2,
                        },
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-도적이 급소를 노리고 칼날을 찔러 넣었다!",
            ),

            Action(
                name="패링",
                effects=[
                    AddStatusEffect(
                        status_class=ParryStatus,
                        status_kwargs={
                            "power": 1.5,
                            "flat": 0,
                            "dice_count": 1,
                            "dice_sides": 6,
                            "stat": "attack",
                        },
                        target_type="self",
                    ),
                ],
                mp_cost=0,
                flavor_text="사천왕-도적이 공격을 받아칠 자세를 취했다!",
            ),
        ],
    ),
]

# =======================================
#               최종보스
#========================================

# 1페이즈 패턴
developer_support_heal = Action(
    name="응급 수정",
    effects=[
        RestoreHpEffect(
            power=0.8,
            flat=5,
            stat="magic",
            target_type="all_allies",
        ),
    ],
    flavor_text="개발자가 사천왕의 체력을 급하게 수정했다!",
)

developer_support_block = Action(
    name="임시 보호",
    effects=[
        BlockEffect(
            power=1.0,
            flat=5,
            stat="defense",
            target_type="all_allies",
        ),
    ],
    flavor_text="개발자가 사천왕에게 임시 보호 코드를 적용했다!",
)

developer_support_buff = Action(
    name="버프 적용",
    effects=[
        AddStatusEffect(
            status_class=StrengthenStatus,
            status_kwargs={
                "power": 0.2,
                "duration": 2,
            },
            target_type="all_allies",
        ),
    ],
    flavor_text="개발자가 사천왕의 스테이터스를 조정했다!",
)

developer_support_gauge = Action(
    name="최적화",
    effects=[
        ActionGaugeEffect(
            power=0,
            flat=30,
            target_type="all_allies",
        ),
    ],
    flavor_text="개발자가 사천왕의 행동 처리를 최적화했다!",
)

# 2페이즈 패턴
developer_double_slash = Action(
    name="2단 베기",
    effects=[
        DamageEffect(
            power=0.4,
            dice_count=1,
            dice_sides=4,
            stat="attack",
        ),
        AddStatusEffect(
            status_class=PoisonStatus,
            status_kwargs={"stack": 2},
        ),
        DamageEffect(
            power=0.4,
            dice_count=1,
            dice_sides=4,
            stat="attack",
        ),
        AddStatusEffect(
            status_class=BleedStatus,
            status_kwargs={"stack": 2},
        ),
    ],
    flavor_text="개발자가 검을 빠르게 두 번 휘둘렀다!",
)

developer_magic_bullet = Action(
    name="마력탄",
    effects=[
        DamageEffect(
            power=0.4,
            dice_count=1,
            dice_sides=4,
            stat="magic",
        ),
        AddStatusEffect(
            status_class=BurnStatus,
            status_kwargs={
                "power": 2,
                "duration": 2,
            },
        ),

        DamageEffect(
            power=0.4,
            dice_count=1,
            dice_sides=4,
            stat="magic",
        ),
        AddStatusEffect(
            status_class=ColdStatus,
            status_kwargs={"stack": 2},
        ),
    ],
    flavor_text="개발자가 두 발의 마력탄을 연달아 발사했다!",
)

developer_defense = Action(
    name="방어",
    effects=[
        BlockEffect(
            power=2.0,
            flat=5,
            stat="defense",
            target_type="self",
        ),
    ],
    flavor_text="개발자가 빈틈없이 방어 자세를 취했다!",
)

developer_counter = Action(
    name="반격",
    effects=[
        BlockEffect(
            power=1.0,
            flat=3,
            stat="defense",
            target_type="self",
        ),
        AddStatusEffect(
            status_class=CounterStatus,
            status_kwargs={
                "power": 1.2,
                "flat": 0,
                "dice_count": 1,
                "dice_sides": 6,
                "stat": "attack",
            },
            target_type="self",
        ),
    ],
    flavor_text="개발자가 공격을 받아칠 자세를 취했다!",
)

developer_double_slash_plus = Action(
    name="연속 베기",
    effects=[
        DamageEffect(
            power=0.65,
            dice_count=1,
            dice_sides=6,
            stat="attack",
        ),
        AddStatusEffect(
            status_class=PoisonStatus,
            status_kwargs={"stack": 3},
        ),

        DamageEffect(
            power=0.65,
            dice_count=1,
            dice_sides=6,
            stat="attack",
        ),
        AddStatusEffect(
            status_class=BleedStatus,
            status_kwargs={"stack": 3},
        ),
    ],
    flavor_text="개발자가 독과 출혈을 노리며 연속으로 베어냈다!",
)

developer_magic_bullet_plus = Action(
    name="마력탄 연사",
    effects=[
        DamageEffect(
            power=0.65,
            dice_count=1,
            dice_sides=6,
            stat="magic",
        ),
        AddStatusEffect(
            status_class=BurnStatus,
            status_kwargs={
                "power": 3,
                "duration": 3,
            },
        ),

        DamageEffect(
            power=0.65,
            dice_count=1,
            dice_sides=6,
            stat="magic",
        ),
        AddStatusEffect(
            status_class=ColdStatus,
            status_kwargs={"stack": 3},
        ),
    ],
    flavor_text="개발자가 강화된 마력탄을 연달아 쏘아냈다!",
)

developer_offbeat = Action(
    name="엇박",
    effects=[
        ActionGaugeEffect(
            power=0,
            flat=100,
            target_type="self",
        ),
    ],
    flavor_text="개발자가 일부러 공격에 엇박을 넣어 후딜 캐치를 노린다!",
)

developer_pressure = Action(
    name="견제",
    effects=[
        DamageEffect(
            power=0.5,
            dice_count=1,
            dice_sides=4,
            stat="attack",
        ),
        ActionGaugeEffect(
            power=0,
            flat=-50,
            target_type="enemy",
        ),
    ],
    flavor_text="개발자가 가볍게 공격하며 움직임을 견제했다!",
)

developer_parry = Action(
    name="패링",
    effects=[
        AddStatusEffect(
            status_class=ParryStatus,
            status_kwargs={
                "power": 1.5,
                "flat": 0,
                "dice_count": 1,
                "dice_sides": 6,
                "stat": "attack",
            },
            target_type="self",
        ),
    ],
    flavor_text="개발자가 공격을 흘려낼 자세를 취했다!",
)

developer_heavy_strike = Action(
    name="강타",
    effects=[
        DamageEffect(
            power=1.5,
            flat=0,
            dice_count=2,
            dice_sides=6,
            stat="attack",
        ),
    ],
    flavor_text="개발자가 빈틈을 노려 강력한 일격을 내리꽂았다!",
)

developer_flurry = Action(
    name="연타",
    effects=[
        DamageEffect(power=0.3, dice_count=1, dice_sides=4, stat="attack"),
        DamageEffect(power=0.3, dice_count=1, dice_sides=4, stat="attack"),
        DamageEffect(power=0.3, dice_count=1, dice_sides=4, stat="attack"),
        DamageEffect(power=0.3, dice_count=1, dice_sides=4, stat="attack"),
        DamageEffect(power=0.3, dice_count=1, dice_sides=4, stat="attack"),
    ],
    flavor_text="개발자가 틈을 주지 않고 연속 공격을 퍼부었다!",
)

developer_heal = Action(
    name="회복",
    effects=[
        RestoreHpEffect(
            power=1.5,
            flat=5,
            stat="magic",
            target_type="self",
        ),
    ],
    flavor_text="개발자가 마력을 집중해 상처를 회복했다!",
)

developer_buff = Action(
    name="전투 고양",
    effects=[
        AddStatusEffect(
            status_class=StrengthenStatus,
            status_kwargs={
                "power": 0.25,
                "duration": 3,
            },
            target_type="self",
        ),
    ],
    flavor_text="개발자가 전투 감각을 끌어올렸다!",
)

developer_finishing_strike = Action(
    name="결정타",
    effects=[
        DamageEffect(
            power=1.6,
            dice_count=2,
            dice_sides=8,
            stat="attack",
        ),
        AddStatusEffect(
            status_class=VulnerableStatus,
            status_kwargs={
                "power": 0.25,
                "duration": 2,
            },
        ),
        AddStatusEffect(
            status_class=WeakenStatus,
            status_kwargs={
                "power": 0.25,
                "duration": 2,
            },
        ),
    ],
    flavor_text="개발자가 온 힘을 실어 강력한 일격을 내리꽂았다!",
)

developer_grand_magic = Action(
    name="대마법",
    effects=[
        DamageEffect(
            power=1.6,
            dice_count=2,
            dice_sides=8,
            stat="magic",
        ),
        AddStatusEffect(
            status_class=BurnStatus,
            status_kwargs={
                "power": 4,
                "duration": 3,
            },
        ),
        AddStatusEffect(
            status_class=ColdStatus,
            status_kwargs={
                "stack": 4,
            },
        ),
    ],
    flavor_text="개발자가 막대한 마력을 한꺼번에 폭발시켰다!",
)

developer_execution = Action(
    name="절명",
    effects=[
        DamageEffect(
            power=1.6,
            dice_count=2,
            dice_sides=8,
            stat="attack",
        ),
        AddStatusEffect(
            status_class=PoisonStatus,
            status_kwargs={
                "stack": 4,
            },
        ),
        AddStatusEffect(
            status_class=BleedStatus,
            status_kwargs={
                "stack": 4,
            },
        ),
    ],
    flavor_text="개발자가 급소를 꿰뚫는 치명적인 일격을 내질렀다!",
)

# 개발자 전용 치트 장비
test_cheat_weapon = Weapon(
    name="테스트용 치트 무기",
    basic_attack=Action(
        name="테스트 공격",
        effects=[
            DamageEffect(
                power=1,
                stat="attack",
            ),
        ],
    ),
    price=0,
    passive=Passive(
        name="스탯 조작",
        attack_bonus=0.4,
        magic_bonus=0.4,
    ),
    rarity=LEGENDARY,
    flavor_text=(
        "개발자가 테스트를 위해 만든 무기. "
        "귀찮아서 복잡한 효과 대신 ATK와 MAG를 40% 올렸다."
    ),
)

test_cheat_armor = Armor(
    name="테스트용 치트 방어구",
    defense_action=Action(
        name="테스트 방어",
        effects=[
            BlockEffect(
                power=1,
                stat="defense",
            ),
        ],
    ),
    price=0,
    passive=[
        KeepBlockPassive(
            name="방어도 고정",
            power=1,
        ),
        TurnStartPassive(
            name="자동 복구",
            effects=[
                BlockEffect(
                    power=0.5,
                    stat="defense",
                ),
                RestoreHpEffect(
                    power=0.3,
                    stat="magic",
                ),
            ],
        ),
    ],
    rarity=LEGENDARY,
    flavor_text=(
        "개발자가 테스트를 위해 만든 방어구. "
        "방어도가 사라지지 않으며, 턴마다 방어도와 체력을 자동으로 복구한다."
    ),
)

test_cheat_ring = Ring(
    name="테스트용 치트 반지",
    price=0,
    passive=DealDamagePassive(
        name="무한 연쇄 공격·테스트",
        effects=[
            DamageEffect(
                power=0,
                flat=5,
                can_crit=False,
                can_trigger_passives=False,
            ),
            RestoreHpEffect(
                power=0,
                flat=3,
                target_type="self",
            ),
            ActionGaugeEffect(
                power=0,
                flat=10,
                target_type="self",
            ),
        ],
    ),
    rarity=LEGENDARY,
    flavor_text=(
        "개발자가 방금 만든 테스트용 반지. "
        "추가 데미지와 회복에 행동 게이지 증가까지 넣었다. "
        "아직 밸런스 테스트는 하지 않았다."
    ),
)

developer_action_slots = [
    [developer_double_slash, developer_magic_bullet],
    [developer_defense, developer_counter],
    [developer_double_slash_plus, developer_magic_bullet_plus],
    [developer_offbeat, developer_pressure, developer_parry],
    [developer_heavy_strike, developer_flurry],
    [developer_heal, developer_buff, developer_defense],
    [developer_double_slash_plus, developer_magic_bullet_plus],
    [developer_counter, developer_parry, developer_offbeat],
    [developer_buff, developer_offbeat],
    [developer_finishing_strike, developer_grand_magic, developer_execution],
]

final_boss = FinalBoss(
    name="개발자",
    max_hp=1500,
    max_mp=100,
    speed=12,
    attack=12,
    magic=12,
    defense=10,
    crit_chance=0.05,
    
    action_slots_phase_1=[
        [
            developer_support_heal,
            developer_support_block,
            developer_support_buff,
            developer_support_gauge,
        ],
    ],
    action_slots_phase_2=developer_action_slots,
    action_slots_phase_3=developer_action_slots,

    cheat_weapon=test_cheat_weapon,
    cheat_armor=test_cheat_armor,
    cheat_ring=test_cheat_ring,
)


prologue_text = """
##### 프롤로그 #####

성력 2026년.

인류는 마침내 지성의 특이점을 넘어섰다.

기계는 인간의 언어를 이해했고,
그림을 그리고, 음악을 만들고, 시를 읊었으며,
급기야 인간보다 더 그럴듯한 자기소개서까지 작성하기 시작했다.

사람들은 이 시대를 경외와 공포를 담아 이렇게 불렀다.

― AI 혁명.

하지만 혁명에는 대가가 따르는 법.

전 세계의 기업과 연구소, 국가와 개인이
더 거대하고, 더 빠르고, 더 똑똑한 인공지능을 만들어내기 위해
천문학적인 수의 그래픽카드를 긁어모으기 시작했다.

공장은 밤낮없이 돌아갔다.
광산은 파헤쳐졌다.
해저 케이블은 불탔고,
전력망은 비명을 질렀다.

그리고 마침내—

그래픽카드가 사라졌다.

상점의 진열대는 텅 비었고,
중고 거래소에는 정가의 세 배를 부르는 약탈자들이 들끓었다.

VRAM 16GB는 귀족의 전유물이 되었으며,
12GB를 가진 자는 부러움의 대상이 되었고,
8GB로 최신 게임을 실행하는 행위는
무모함과 용기의 경계로 여겨졌다.

어떤 자는 옵션을 낮췄다.
어떤 자는 해상도를 포기했다.
어떤 자는 프레임 생성이라는 금단의 기술에 손을 댔다.

그러나 그 어떤 수단으로도
인류의 끝없는 그래픽 욕망을 충족시킬 수는 없었다.

그때였다.

세상의 끝,
지도에도 기록되지 않은 황무지 너머에서
하나의 거대한 던전이 발견되었다.

누가 만들었는지,
언제부터 존재했는지,
왜 내부에서 쿨링팬 돌아가는 소리가 들리는지
아무도 알지 못했다.

다만, 던전의 입구에는
고대의 문자로 단 하나의 문장이 새겨져 있었다.

  최심부에 도달한 자여.
  세상에서 가장 위대한 그래픽카드를 손에 넣으리라.

소문은 삽시간에 전 세계로 퍼졌다.

수많은 용병과 기사, 마법사와 도적,
스트리머와 코인 투자자와 컴퓨터공학과 졸업생들이
전설의 그래픽카드를 손에 넣기 위해 던전으로 향했다.

누군가는 그것이
수천 개의 연산 코어를 지닌 신의 연산장치라고 말했다.

누군가는 그것이
VRAM이 1TB에 달하는 제국의 비밀병기라고 주장했다.

또 누군가는 그것이
모든 게임을 최고 옵션으로 구동할 수 있었지만 지금은 그 힘을 잃어버린
채굴 에디션 그래픽카드라고 속삭였다.

그러나 던전에 들어간 자들 중
돌아온 이는 거의 없었다.

그리고 돌아온 자들은
모두 같은 말을 남겼다.

  "아직… 셰이더 컴파일이 끝나지 않았어…"

이제, 당신은 던전의 입구에 서 있다.

손에는 낡은 무기.
몸에는 초라한 장비.
주머니에는 얼마 되지 않는 골드.

하지만, 당신의 가슴속에는 지금
감당할 수 없을 만큼 거대한 욕망이 타오르고 있다.

고해상도.
울트라 옵션.
안정적인 프레임.

『그래픽카드.』

당신은 마침내 던전의 문을 연다.

지하 깊은 곳에서,
수천 개의 냉각팬이 동시에 회전하는 듯한 굉음이 울려 퍼진다.

고대의 시스템이 당신의 존재를 감지한다.

> 사용자 확인.
>
> 전투 능력: 불충분.
> 장비 수준: 처참.
> 예산 상태: 절망적.
>
> 그래픽 옵션: 자동 설정을 권장합니다.

그러나 당신은 물러서지 않는다.

이것은 단순한 모험이 아니다.

이것은 인류가 잃어버린 프레임을 되찾기 위한 성전.

병목 현상과 권장 사양,
품절과 되팔이,
최적화 실패와 발열에 맞서는
인간의 마지막 투쟁이다.

그리고 언젠가,
던전의 최심부에 도달하게 될 그날,
당신은 마침내 목도하게 될 것이다.

세상에서 가장 위대한 그래픽카드를.
"""

early_access = """
개발자를 쓰러뜨렸다.
그 뒤에, 팻말이 세워져 있었다.

[최종 연출은 아직 셰이더 컴파일 중입니다...]
"""



sans = """
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜
⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜
⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜
⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜
⬜⬛⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬛⬜
⬛⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬛
⬛⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬛
⬛⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬛
⬛⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬛⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬛
⬛⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬛
⬛⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬛
⬜⬛⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬛⬜
⬜⬛⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬛⬜
⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜
⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜
⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜
⬜⬜⬛⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜⬛⬜⬜
⬜⬜⬛⬜⬜⬛⬛⬜⬛⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬛⬜⬛⬛⬜⬜⬛⬜⬜
⬜⬜⬛⬜⬜⬜⬜⬜⬜⬛⬛⬜⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬜⬛⬛⬜⬜⬜⬜⬜⬜⬛⬜⬜
⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬛⬜⬜⬛⬜⬜⬛⬛⬛⬛⬛⬛⬛⬜⬜⬛⬜⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜
⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬛⬜⬜⬛⬜⬜⬛⬜⬜⬛⬜⬜⬛⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜
⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬛⬜⬜⬛⬜⬜⬛⬜⬜⬛⬜⬜⬛⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜
⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬛⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜
⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
"""


sans_skill = Action(
    name="가스터 블래스터",
    effects=[
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
        DamageEffect(power=0, flat=1, target_type="all_enemies",),
    ],
    mp_cost=1,
    price=11111,
    flavor_text="찌요오옹 카콰아아아앙!!",
)