from pyteal import *


class CarSpot:
    class Variables:
        name = Bytes("NAME")
        description = Bytes("DESCRIPTION")
        image = Bytes("IMAGE")
        amount = Bytes("AMOUNT")
        owner = Bytes("OWNER")
        likes = Bytes("LIKES")
        isBought = Bytes("ISBOUGHT")
        liked = Bytes("LIKED")

    class AppMethods:
        buy = Bytes("buy")
        sell = Bytes("sell")
        like = Bytes("like")
        dislike = Bytes("dislike")

    # allow users to create a new car 
    def application_creation(self):
        return Seq([
            # checks if input data in application_args are not empty/invalid values
            Assert(
                And(
                    Txn.application_args.length() == Int(4),
                    Txn.note() == Bytes("car-spot:uv1"),
                    Btoi(Txn.application_args[3]) > Int(0),
                    Len(Txn.application_args[0]) > Int(0),
                    Len(Txn.application_args[1]) > Int(0),
                    Len(Txn.application_args[2]) > Int(0),
                )
            ),
            App.globalPut(self.Variables.name, Txn.application_args[0]),
            App.globalPut(self.Variables.description, Txn.application_args[1]),
            App.globalPut(self.Variables.image, Txn.application_args[2]),
            App.globalPut(self.Variables.amount,
                          Btoi(Txn.application_args[3])),
            App.globalPut(self.Variables.owner, Txn.sender()),
            App.globalPut(self.Variables.likes,
                          Int(0)),
            App.globalPut(self.Variables.isBought,
                          Int(0)),
            Approve()
        ])

    # function(subroutine) to be called when opting in the app
    def optIn(self):
        # Sets the local Boolean value of liked for sender to false which is Int 0
        return Seq([
            App.localPut(Txn.sender(), self.Variables.liked, Int(0)),
            Approve()
        ])

    # allow users to buy a car that hasn't yet been bought
    def buy(self):
        return Seq([
            # checks if car is on sale
            # checks if sender is not the car's owner
            Assert(
                And(
                    Global.group_size() == Int(2),
                    Txn.application_args.length() == Int(2),
                    App.globalGet(self.Variables.isBought) == Int(0),
                    App.globalGet(self.Variables.owner) != Txn.sender(),
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

    # allow car owners to sell a car
    def sell(self):
        return Seq([
            # checks if sender is the car's owner
            # checks if car isn't already on sale
            Assert(
                And(
                    Global.group_size() == Int(1),
                    Txn.application_args.length() == Int(2),
                    App.globalGet(self.Variables.isBought) == Int(1),
                    App.globalGet(self.Variables.owner) == Txn.sender(),
                ),
            ),
            App.globalPut(self.Variables.isBought, Int(0)),
            Approve()
        ])

    # allow users to like  a car
    def like(self):
        return Seq([
            # checks if sender has already liked the car
            Assert(
                And(

                    Global.group_size() == Int(1),
                    Txn.application_args.length() == Int(1),
                    App.localGet(Txn.sender(), self.Variables.liked) == Int(0),
                ),
            ),
            App.localPut(Txn.sender(), self.Variables.liked, Int(1)),
            App.globalPut(self.Variables.likes, App.globalGet(
                self.Variables.likes) + Int(1)),
            Approve()
        ])

    # allow users to dislike a car they had previously liked
    def dislike(self):
        return Seq([
            # checks if sender has already liked the car
            Assert(
                And(
                    Global.group_size() == Int(1),
                    Txn.application_args.length() == Int(1),
                    App.localGet(Txn.sender(), self.Variables.liked) == Int(1),
                ),
            ),
            App.localPut(Txn.sender(), self.Variables.liked, Int(0)),
            App.globalPut(self.Variables.likes, App.globalGet(
                self.Variables.likes) - Int(1)),
            Approve()
        ])

    def application_deletion(self):
        return Return(Txn.sender() == Global.creator_address())

    def application_start(self):
        return Cond(
            [Txn.application_id() == Int(0), self.application_creation()],
            [Txn.on_completion() == OnComplete.DeleteApplication,
             self.application_deletion()],
            [Txn.on_completion() == OnComplete.OptIn, self.optIn()],
            [Txn.application_args[0] == self.AppMethods.buy, self.buy()],
            [Txn.application_args[0] == self.AppMethods.sell, self.sell()],
            [Txn.application_args[0] == self.AppMethods.like, self.like()],
            [Txn.application_args[0] == self.AppMethods.dislike, self.dislike()],

        )

    def approval_program(self):
        return self.application_start()

    def clear_program(self):
        return Return(Int(1))
