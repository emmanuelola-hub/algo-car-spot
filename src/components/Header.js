const Header = ({balance}) => {
  return (
    <header>
      <div className="d-flex flex-column flex-md-row align-items-center pb-3 mb-4 border-bottom">
        <a
          href="/"
          className="d-flex align-items-center text-dark text-decoration-none"
        >
          <h2 className="fs-4">CAR SPOT</h2>
        </a>
        <nav className="d-inline-flex mt-2 mt-md-0 ms-md-auto">
          <a className="py-2 text-dark text-decoration-none" href="#">
           Balance: {balance / 1000000} ALGO 
          </a>
        </nav>
      </div>
      <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
        <h1 className="display-4 fw-normal">Car Spot</h1>
        <p className="fs-5 text-muted">
          Join us in creating the next generation of car NFTs
        </p>
      </div>
    </header>
  );
};

export default Header;
