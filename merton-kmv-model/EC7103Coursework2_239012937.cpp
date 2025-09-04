/**********************************************************************************************************************************************                                                     
                                                        The Merton-KMV Model

The KMV-Merton model is a widely used financial model for assessing credit risk. It provides a framework to calculate the 
distance to default (DTD) of a firm by analyzing the relationship between its asset value and its liabilities. The model 
considers the firm's capital structure, equity value, debt obligations, risk-free rate, and volatility of assets to determine the likelihood of 
default within a given time frame. Through iterative techniques like the Newton-Raphson method, it refines estimates of asset value and 
volatility until convergence, aiding in the accurate assessment of a firm's financial health and creditworthiness.

The model views equity as a call option placed on the assets of the firm, with an exercise price given by the face value of debt. One of the 
measures calculated is the Distance to Default (DTD), which depicts how far the firm's asset value can decline before it becomes insolvent 
and unable to meet its debt obligations. This is analogous to the call option expiring out of money. Hence, the Black-Scholes formula provides 
a mathematical framework for valuing credit risk. The value of equity is thus given by;
 
                                                        E = A * N(d1) - D * e^(-r*T) * N(d2)

 where,  
                                             d1 = ( log(V/D) + (R + sigma_V ^2/2)*T ) / (sigma_V * sqrt(T),
                                                           d2 = d1 - sigma_V * sqrt(T)

 A = Firm value or asset value today (will be used interchangeably in the code)
 E = Value of company's equity today
 D = Value of company's debt today
 sigma_V = Volatility of assets
 N(x) = The cumulative normal distribution function.

Distance to Default (d1) captures how many standard deviations away a firm is from the default.

The Newton-Raphson method is a numerical tehnque used to find the roots of a function, or in other words, to solve for equations of the form 
f(x)=0. In the context  of the Merton-KMV model, we are using it to iteratively refine our estimates of the asset value and volatility until
it converges to a solution, as they are not directly observable.
Here's how this works in the following code:

    1. Initialization: The function 'newton_raphson_algorithm' (given as a separate algorithm), is called with initial parameters such as equity, 
       volatility of equity, debt, risk-free rate, and time to maturity.

    2. Iteration: Inside the function, we start an iterative process. We iterate through a loop (for loop) where we perform calculations to 
       update our estimates of the asset value and volatility.

    3. Calculations: Within each iteration of the loop, we perform calculations to update the values of A (asset value), 
       sigma_A (volatility of the asset), d1, and d2 (parameters in the Merton model). These calculations involve formulas based on the 
       Merton model and the Newton-Raphson method.
    
    4. Convergence Check: After each iteration, we check whether our new estimates of the asset value and volatility have converged to within 
       a certain tolerance (new_tol). If they have, we consider the solution converged and exit the loop.

    5. Output and Return: If convergence is achieved, we output the firm value, volatility, distance to default, number of iterations, and 
       tolerance. If convergence is not achieved after a certain number of iterations, we return a code indicating failure to converge. 
       Otherwise, we return a code indicating convergence.

Overall, the Newton-Raphson method contributes to the KMV-Merton method by providing a means to iteratively refine our estimates of the 
asset value and volatility until we converge to a solution that satisfies the convergence criteria. The goal is to find the asset value 
and volatility that best match the observed market conditions and result in accurate estimates of the firm's value, distance to default 
KMV distance to default.

(KMV Distance to default interpretation: A higher DTD indicates a larger financial buffer or distance between the firm's asset value 
and its debt obligations compared to the level of asset volatility. This suggests that the firm can withstand greater fluctuations 
in asset values without risking default, reflecting a stronger financial position and lower credit risk.)

***********************************************************************************************************************************************/


#include <iostream> /*Brings in features such as readng data and printing results to the console. It is used to prompt the user to input values 
required for calculation.*/

#include <cmath> /* Includes mathematical functions like sqrt, log, exp, and erf for calculations, each of which are used for different purposes
within the code.*/

using namespace std; // Avoids having to write std:: before elements from the standard library.

/* Function to compute cumulative distribution function for standard normal distribution. It's used here to estimate probabilities related to 
asset values and potential default. It is declared globally so that it is accessible from anywhere within the code.*/

double N(double x) {
    return 0.5 * (1 + erf(x / sqrt(2)));
}

// Newton-Raphson method for finding asset value and volatility.
int newton_raphson_algorithm(double E, double D, double T, double r, double sigma_E) {
    int n = 10000; //Defines the number of points to search within a specific range of asset value (A).
    int inner_iter = 1000; //Sets the maximum number of iterations within each outer loop to refine the estimates of firm value and volatility.

    double old_tol = 1e1; /*(Initial tolerance) Establishes the initial threshold for convergence. The difference between estimated and actual 
    values (A_diff and sigma_E_diff) should be less than old_tol for convergence.*/

    int outer_iter = 10000; //Defines the maximum number of attempts to find a solution within the specified tolerance.
    double epsilon = 0.00001; //To avoid division by zero in some calculations.
    double new_tol = 0.0; //Updated tolerance

    double A, sigma_A, d1, d2, kmv_dtd, A_diff, sigma_E_diff; // Variables for calculations

    int iterations_to_convergence = 0; //Tracks iterations needed for convergence.

    bool converged = false; /*Flag indicating if convergence has been reached. Basically, used to control the flow of the program and determine 
    whether or not to continue iterating.*/

    //Outer loop for iterative search of asset value.
    for (int i = 1; i <= outer_iter; i++) {
        bool found_better_solution = false; // To set flag to prevent printing subsequent solutions.

    //Inner loop for iterative search of volatility
        for (int j = 1; j <= inner_iter; j++) {
            A = E + D/2 + (i/n)*D; //Initiating a guess for firm value.
            sigma_A = 0.05 + (j/inner_iter)*(1.0 - epsilon); //Initiating a guess for volatility of firm value.
            d1 = (log(A/D) + (r+sigma_A*sigma_A/2.)*T)/(sigma_A*sqrt(T)); // Calculate d1 i.e., distance to default.
            d2 = d1 - sigma_A*sqrt(T); //Calculate d2
            kmv_dtd = (A-D) / sigma_A; //Calculate KMV distance to default.
           
            /*'A-diff' is the relative difference between the expected value of the assets and the sum of the the debt and equity.
               Basically, how far the current estimate estimate of the firm value is from the expected value, relative to the firm value itself. 
               'A*N(d1)' represents the value of assets that accrues to the equity holder,
               'D*exp(-r*T)*N(d2)' represents the present value of debt,
               'E' represents the initial equity value. 
               Dividing by A normalizes the difference by the current value of asset, making it a relative difference.*/
            A_diff = (A*N(d1) - D*exp(-r*T)*N(d2) - E)/A; 

            /*'sigma_E_diff' is the difference between the current estimate of the asset volatility and the target or expected value of the asset 
               volatility.
               'A/E' helps normalize the difference by the firm's financial structure,
               'sigma_A' represents the current estimate of the firm's asset volatility,
               'sigma_E' is the target value of firm's asset volatility.*/
            sigma_E_diff = A/E * N(d1) * sigma_A - sigma_E;

            new_tol = abs(A_diff) + abs(sigma_E_diff); //Updated tolerance is the sum of absolute value of the differences given above.


            /*The if statement if the current total difference is smaller than the previous tolerance, if yes, then it means that the 
            estimates are closer to the ideal values, and hence the current tolerance is updated to reflect the improvement. */
            if (new_tol < old_tol) {
                old_tol = new_tol;
                iterations_to_convergence = i * inner_iter + j; //The number of iterations needed to reach this level of improvement is tracked.
                converged = true; //A flag is set to indicate that convergence might have been achieved.

                //Prints the results in the console.
                cout << "Firm Value: $" << A << endl;
                cout << "\nVolatility of Firm Value: " << sigma_A << endl;
                cout << "\nDistance to Default: " << d1 << endl;
                cout << "\nKMV Distance to Default: " << kmv_dtd << endl;
                cout << "\nIterations to Convergence: " << iterations_to_convergence << endl;
                cout << "\nTolerance: " << new_tol << endl;
                found_better_solution = true; // Set flag to prevent printing subsequent solutions
            }

        /* The inner loop continues iterating as long as j is less than or equal to inner_iter. 
          The outer loop continues iterating as long as i is less than or equal to outer_iter.
          This allows for refining within each outer loop iteration and exploring different possible asset values, respectively.
        */

        }
    }

    if (converged) {
        return 0; // Convergence achieved meaning a solution was potentially found.
    } else if (iterations_to_convergence >= 1000 * inner_iter) {
        return 1; // Convergence not achieved within the set limit.
    } else {
        return 2; // Variance converges to a negative value (unrealsitic scenario)
    }
}

/*The main function acts as a user interface in this case, as it collects input data, 
calls the core calculation function, and interprets the results based on the returned code.*/

int main() {
    double E, D, T, r, sigma_E;

    // Input parameters
    cout << "Enter equity value: $";
    cin >> E;
    cout << "Enter debt value: $";
    cin >> D;
    cout << "Enter time to maturity (in years): ";
    cin >> T;
    cout << "Enter risk-free rate (as a decimal): ";
    cin >> r;
    cout << "Enter volatility of equity (as a decimal): ";
    cin >> sigma_E;

    // Call the KMV Merton algorithm. It passes the five input values as arguments to the function.
    int result = newton_raphson_algorithm(E, D, T, r, sigma_E);
    
    // Print the result in the console.
    if (result == 0) {
        cout << "Convergence achieved." << endl;
    } else if (result == 1) {
        cout << "Convergence not achieved after 1000 iterations." << endl;
    } else {
        cout << "Variance converges to a negative value." << endl;
    }
    
    return 0;
}
