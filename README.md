# FinCore-2.0

I have difficulty with documentation.
(I'll try to improve over time)

Money management project
- Commitment to applying DDD
- SOLID Principles
- Explicit typing code
- Invariant treatment


## Domain class hierarchy:
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


**detail**
> command != instruction
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
< quickedit >>> Family/Gabriel/Wallet/Travels/To_Paris/With_my_girlfrien/...:
# All after the second bar is considered a vault inside other vault, inside other vault etc.
```

P.S.: I want to change it soon, because, if you can see it, you have to tell in what group you want to add a person or what person in what group you're using to add a vault etc.

### Operations

```python
# OperationKind.ASSIGN
# Structure -> <path>: <expr>
< quickedit >>> Family/Gabriel/Wallet: 10
# Create a new Money(10) in Vault

# create a new person or vault is an assign operation
< quickedit >>> Family: Gabriel
< quickedit >>> Family/Gabriel/Wallet: To_Paris
# create a new group is other type of operation

# - - -

# OperationKind.GROUP_CREATE
# Structure -> groups: <expr>
< quickedit >>> groups: Friends
# It's because the treatment between groups and person, vaults, etc. is different. You can see it in: GroupCreateHandler and AssignHandler
```
