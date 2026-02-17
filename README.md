# FinCore-2.0

I have difficulty with documentation.
(I'll try to improve over time)

Money management project
- Commitment to applying DDD
- SOLID Principles
- Explicit typing code
- Invariant treatment

## Description
CLI money management project

## Domain
Is this part necessary?

### Aggregates

**GroupAggregate**
Description: GroupAggregate is the aggregate root, used to handle the unique EntityMap that contains all the groups, encapsulating all the work rules involving them.
```python
GroupAggregate(
    groups: EntityMap[Group]
)
```

### Entities

**DomainEntity** `Structure, not abstract class`
```python
DomainEntity(
    id: EntityId,
    name: EntityName,
    children: EntityMap[DomainEntity]
)
```

**Group**
```python
Group(
    id: EntityId,
    name: GroupName,
    members: EntityMap[Person]
)
```

**Person**
```python
Person(
    id: EntityId,
    name: PersonName,
    members: EntityMap[Vault]
)
```

**Vault**
```python
Vault(
    id: EntityId,
    name: VaultName,
    vaults: EntityMap[Vault],
    values: Sequence[Money | ScaledMoney]
)
```

### ValueObjects

Characteristics:
- Do not have ID (EntityId)
- Usually, is a dataclass
- Immutable

**Money**
Description: In the future, may I defy as BRLMoney, because it's the format I'm using now (R$5,00 [reais, centavos]). But, for now, have it in mind.
```python
Money(
    reais: int,
    centavos: int
)
```

**ScaledMoney**
Description: It exists because I'm considering to show how many "banknotes" is there instead just to create a global amount. May I make the Money just let pass fix values (1, 2, 5, 10, 20 etc.).
```python
ScaledMoney(
    money: Money,
    factor: int
)
```

**EntityName**
Characteristics:
- Not commit Non-alphanumerics + "_"
```
name: yes
NAME: yes
Name: yes
NameSurname: yes
Name_Surname: yes
Name123: yes
Name_123%: not
```

Types:
- GroupName
- PersonName
- VaultName

```python
EntityName(
    _value: str
)
```


## Domain class hierarchy
- GroupAggregate
- Group
- Person
- Vault (may contain others of the same class)
- ScaledMoney ($5.00 * factor)
- Money

## Intended use:

**CLI commands**
- /change_group
- /current_group (shows the the group you're editing)
- /quickedit | qe (main editor)
`>>> command here`


**detail**: command != instruction
```python
`Command: str # Perhaps encapsulate it later.

Instruction:
    RawInstruction(_data: str)
    AnalyzedInstruction(
        path: InstructionPath,
        operation: InstructionOperation
    )
```


command is the name used to refer what you type in this first cli, instructions is what you type in Quickedit.


**Instruction structure examples**
> group/person/vault/inner_vault

**Attention**: You can't modify ValueObject directly, at least:
> group/person/vault: 10 <- Money
> group/person/vault: 10 * 5 <- ScaledMoney

**Instructions and their relation with the classes**
```python
# Structure -> groups: group
< quickedit >>> groups: Family
# Create a new Group in GroupAggregate

# Structure -> group: person
< quickedit >>> Family: Gabriel
# Create a new Person in Group

# Structure -> group/person: vault
< quickedit >>> Family/Gabriel: Wallet
# Create a new Vault in Person

# Structure -> group/person/vault: inner_vault
< quickedit >>> Family/Gabriel/Wallet: Travels
# Create a new Vault in Vault

# You could create how many inner vaults you want, like:
< quickedit >>> Family/Gabriel/Wallet/Travels/To_Paris/With_my_girlfriend/...:
# All after the second bar is considered a vault inside other vault, inside other vault etc.
```

P.S.: I want to change it soon, because, if you can see it, you have to tell in what group you want to add a person or what person in what group you're using to add a vault etc.

### Operations

```python
# OperationKind.ASSIGN
# Structure = <path>: <expr>
< quickedit >>> Family/Gabriel/Wallet: 10
# Create a new Money(10) in Vault

# create a new person or vault is an assign operation
< quickedit >>> Family: Gabriel
< quickedit >>> Family/Gabriel/Wallet: To_Paris
# create a new group is other type of operation

# - - -

# OperationKind.GROUP_CREATE
# Structure = groups: <expr>
< quickedit >>> groups: Friends
# It's because the treatment between groups and person, vaults, etc. is different. You can see it in: GroupCreateHandler and AssignHandler

# - - -

# OperationKind.REKEY
# Structure = <path> -> <expr>
< quickedit >>> Family -> Friends
< quickedit >>> Family/Ana -> Anna
< quickedit >>> Family/Anna/Walet -> Wallet
# Change the name (rekey)
# Thinking in make "=>" to transactions
```
