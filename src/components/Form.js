import { useState } from "react";
import { stringToMicroAlgos } from "../utils/conversions";

const Form = ({ addCar }) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImageUrl] = useState("");
  const [amount, setAmount] = useState("");

  const formHandler = (e) => {
    e.preventDefault();
    addCar({name, description, image, amount: stringToMicroAlgos(amount) });
  };
  return (
    <div
      className="modal modal-signin position-static d-block py-5"
      tabIndex={-1}
      role="dialog"
      id="modalSignin"
    >
      <div className="modal-dialog" role="document">
        <div className="modal-content rounded-5">
          <div className="modal-header p-5 pb-4 border-bottom-0">
            {/* <h5 class="modal-title">Modal title</h5> */}
            <h2 className="fw-bold mb-0">Add Car</h2>
          </div>
          <div className="modal-body p-5 pt-0">
            <form onSubmit={formHandler}>
              <div className="form-floating mb-3">
                <input
                  type="text"
                  className="form-control rounded-4"
                  id="floatingInput"
                  placeholder="Name of Car"
                  onChange={(e) => setName(e.target.value)}
                />
                <label htmlFor="floatingInput">Name of Car</label>
              </div>
              <div className="form-floating mb-3">
                <input
                  type="text"
                  className="form-control rounded-4"
                  id="floatingInput"
                  placeholder="Description"
                  onChange={(e) => setDescription(e.target.value)}
                />
                <label htmlFor="floatingInput">Description</label>
              </div>
              <div className="form-floating mb-3">
                <input
                  type="text"
                  className="form-control rounded-4"
                  id="floatingInput"
                  placeholder="Image URL"
                  onChange={(e) => setImageUrl(e.target.value)}
                />
                <label htmlFor="floatingInput">Image URL</label>
              </div>
              <div className="form-floating mb-3">
                <input
                  type="text"
                  className="form-control rounded-4"
                  id="floatingInput"
                  placeholder="Amount"
                  onChange={(e) => setAmount(e.target.value)}
                />
                <label htmlFor="floatingInput">Amount</label>
              </div>
              <button
                className="w-100 mb-2 btn btn-lg rounded-4 btn-primary"
                type="submit"
              >
                Add Car
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Form;
