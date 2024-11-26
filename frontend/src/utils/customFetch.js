import router from "@/router/index"

const BASE_URL = 'http://127.0.0.1:5000'

export const customFetch = async (url = '/', options = {auth : true}) => {
    const origin = BASE_URL;
    
    // Parse the stored user to get the authentication token
    const user = JSON.parse(localStorage.getItem('user'));
    const authToken = user?.['token']; // Get the auth token, if it exists
  
    // If authentication is required and no token is found, handle accordingly
    if (options.auth && !authToken) {
      console.error('Authentication token is missing.');
      // Optionally, redirect to login or return an error
      router.push('/login');
      return;
    }
  
    // Build the full request options object
    const fetchOptions = {
      method: (options.body && !options.method) ? 'POST' : options.method ?? 'GET', // Default to GET method
      headers: {
        'Content-Type': 'application/json',
        // 'Access-Control-Allow-Origin' : ,
        ...(authToken ? { 'Authentication-Token': authToken } : {}), // Include token if available
        ...options.headers, // Merge additional headers if provided
      },
      ...(options.body ? { body: options.body } : {}), // direcly send body, stringify it in the custom itself
      ...options, // Merge any other options provided
    };
  
    try {
      // Make the fetch request
      const res = await fetch(`${origin}${url}`, fetchOptions);
  
      // If response is forbidden, redirect to login
      if (res.status === 403 || res.status === 405) {
        router.push('/login');
        return;
      }
  
      return res; // Return the response object
  
    } catch (error) {
      console.error('Fetch error:', error);
      // Handle errors (e.g., network issues)
      throw error;
    }
  };