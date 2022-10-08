from pyteal import *

from spotter_contract import CarSpot

if __name__ == "__main__":
    approval_program = CarSpot().approval_program()
    clear_program = CarSpot().clear_program()

    # Mode.Application specifies that this is a smart contract
    compiled_approval = compileTeal(approval_program, Mode.Application, version=6)
    print(compiled_approval)
    with open("spotter_approval.teal", "w") as teal:
        teal.write(compiled_approval)
        teal.close()

    # Mode.Application specifies that this is a smart contract
    compiled_clear = compileTeal(clear_program, Mode.Application, version=6)
    print(compiled_clear)
    with open("spotter_clear.teal", "w") as teal:
        teal.write(compiled_clear)
        teal.close()