from pyteal import *


class CarSpot:
    class Variables:
        name = Bytes("NAME")
        description = Bytes("DESCRIPTION")
        image = Bytes("IMAGE")
        amount = Bytes("AMOUNT")
        owner = Bytes("OWNER")
        likes = Bytes("LIKES")
        dislikes = Bytes("DISLIKES")
        isBought = Bytes("ISBOUGHT")

    class AppMethods:
        buy = Bytes("buy")
        sell = Bytes("sell")
        like = Bytes("like")
        dislike = Bytes("dislike")

    def application_creation(self):
        return Seq([
            Assert(Txn.application_args.length() == Int(5)),
            Assert(Txn.note() == Bytes("car-spot:uv1")),
            Assert(Btoi(Txn.application_args[3]) > Int(0)),
            # set variables name description image and amount
            App.globalPut(self.Variables.name, Txn.application_args[0]),
            App.globalPut(self.Variables.description, Txn.application_args[1]),
            App.globalPut(self.Variables.image, Txn.application_args[2]),
            App.globalPut(self.Variables.amount,
                          Btoi(Txn.application_args[3])),
            App.globalPut(self.Variables.owner, Txn.sender()),
            App.globalPut(self.Variables.likes,
                          Int(0)),
            App.globalPut(self.Variables.dislikes,
                          Int(0)),
            App.globalPut(self.Variables.isBought,
                          Int(0)),
            Approve()
        ])

    # buy function
    def buy(self):
        return Seq([
            #check group size is equal to two, args is 2 and check if car has already been bought
            Assert(
                And(
                    Global.group_size() == Int(2),
                    Txn.application_args.length() == Int(2),
                    App.globalGet(self.Variables.isBought) == Int(0)
                ),
            ),
            Assert(
                And(
                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == App.globalGet(
                        self.Variables.owner),
                    Gtxn[1].amount() == App.globalGet(self.Variables.amount),
                    Gtxn[1].sender() == Gtxn[0].sender(),
                )
            ),

            App.globalPut(self.Variables.owner, Gtxn[1].sender()),
            App.globalPut(self.Variables.isBought, Int(1)),
            Approve()
        ])

    # sell function
    def sell(self):
        return Seq([
            Assert(
                # check group size, args and make sure that car has been bought
                And(
                    Global.group_size() == Int(1),
                    Txn.application_args.length() == Int(2),
                    App.globalGet(self.Variables.isBought) == Int(1),
                    #check if is owner
                    App.globalGet(self.Variables.owner) == Txn.sender(),
                ),
            ),
            App.globalPut(self.Variables.isBought, Int(0)),
            Approve()
        ])

    def like(self):
        return Seq([
            #check the group size and arg length
            Assert(
                And(
                    Global.group_size() == Int(1),
                    Txn.application_args.length() == Int(1),
                    # owners cant like or dislike
                    App.globalGet(self.Variables.owner) != Txn.sender(),
                ),
            ),

            App.globalPut(self.Variables.likes, App.globalGet(self.Variables.likes) + Int(1)),
            Approve()
        ])

    def dislike(self):
        return Seq([
            Assert(
                And(
                    Global.group_size() == Int(1),
                    Txn.application_args.length() == Int(1),
                    # owners cant like or dislike
                    App.globalGet(self.Variables.owner) != Txn.sender(),
                ),
            ),

            App.globalPut(self.Variables.dislikes, App.globalGet(self.Variables.dislikes) + Int(1)),
            Approve()
        ])

    def application_deletion(self):
        return Return(Txn.sender() == Global.creator_address())

    def application_start(self):
        return Cond(
            [Txn.application_id() == Int(0), self.application_creation()],
            [Txn.on_completion() == OnComplete.DeleteApplication,
             self.application_deletion()],
            [Txn.application_args[0] == self.AppMethods.buy, self.buy()],
            [Txn.application_args[0] == self.AppMethods.sell, self.sell()],
            [Txn.application_args[0] == self.AppMethods.like, self.like()],
            [Txn.application_args[0] == self.AppMethods.dislike, self.dislike()],

        )

    def approval_program(self):
        return self.application_start()

    def clear_program(self):
        return Return(Int(1))


