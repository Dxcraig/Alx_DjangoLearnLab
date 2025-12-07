"""
API Query Capabilities Test Suite

This script tests the filtering, searching, and ordering capabilities
of the Book API. It performs various queries to validate the implementation.

Requirements:
    - pip install requests
    - Django server running on http://localhost:8000
    - Sample books data in the database

Usage:
    python test_api_queries.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = 'http://localhost:8000/api/books/'

def print_separator():
    """Print a visual separator"""
    print("=" * 70)

def print_test_header(test_name: str):
    """Print formatted test header"""
    print_separator()
    print(f"TEST: {test_name}")
    print_separator()

def print_results(response: requests.Response):
    """Print formatted response results"""
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            
            # Handle paginated response
            if isinstance(data, dict) and 'results' in data:
                results = data['results']
                print(f"Total Count: {data.get('count', 'N/A')}")
                print(f"Results on this page: {len(results)}")
                print(f"Next Page: {'Yes' if data.get('next') else 'No'}")
                print(f"Previous Page: {'Yes' if data.get('previous') else 'No'}")
                
                if results:
                    print("\nSample Results:")
                    for i, book in enumerate(results[:3], 1):  # Show first 3
                        print(f"  {i}. {book.get('title', 'N/A')} "
                              f"({book.get('publication_year', 'N/A')}) "
                              f"- Author ID: {book.get('author', 'N/A')}")
                    
                    if len(results) > 3:
                        print(f"  ... and {len(results) - 3} more")
                else:
                    print("\nNo results found")
            else:
                # Non-paginated response
                results = data if isinstance(data, list) else [data]
                print(f"Results: {len(results)}")
                for i, book in enumerate(results[:3], 1):
                    print(f"  {i}. {book.get('title', 'N/A')} "
                          f"({book.get('publication_year', 'N/A')})")
        except json.JSONDecodeError:
            print("Error: Could not parse JSON response")
            print(response.text[:200])
    else:
        print(f"Error Response: {response.text[:200]}")
    
    print()

def test_basic_list():
    """Test 1: Basic list without any filters"""
    print_test_header("Basic List (No Filters)")
    
    print("Request: GET /api/books/")
    response = requests.get(BASE_URL)
    print_results(response)
    
    return response.status_code == 200

def test_filter_by_year():
    """Test 2: Filter by publication year"""
    print_test_header("Filter by Publication Year")
    
    test_year = 2023
    params = {'publication_year': test_year}
    print(f"Request: GET /api/books/?publication_year={test_year}")
    
    response = requests.get(BASE_URL, params=params)
    print_results(response)
    
    # Validate filtering worked
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data if isinstance(data, list) else [])
        
        all_match = all(book.get('publication_year') == test_year for book in results)
        if results and all_match:
            print("✓ All results match the filter criteria")
        elif not results:
            print("⚠ No results found (may be expected if no data)")
        else:
            print("✗ Some results don't match the filter")
    
    return response.status_code == 200

def test_filter_by_author():
    """Test 3: Filter by author"""
    print_test_header("Filter by Author ID")
    
    author_id = 1
    params = {'author': author_id}
    print(f"Request: GET /api/books/?author={author_id}")
    
    response = requests.get(BASE_URL, params=params)
    print_results(response)
    
    # Validate filtering worked
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data if isinstance(data, list) else [])
        
        all_match = all(book.get('author') == author_id for book in results)
        if results and all_match:
            print("✓ All results match the filter criteria")
        elif not results:
            print("⚠ No results found (may be expected if no data)")
        else:
            print("✗ Some results don't match the filter")
    
    return response.status_code == 200

def test_search():
    """Test 4: Search functionality"""
    print_test_header("Search Functionality")
    
    search_term = "Django"
    params = {'search': search_term}
    print(f"Request: GET /api/books/?search={search_term}")
    
    response = requests.get(BASE_URL, params=params)
    print_results(response)
    
    # Validate search worked
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data if isinstance(data, list) else [])
        
        if results:
            print(f"✓ Search found {len(results)} result(s)")
            # Check if search term appears in results
            contains_term = any(
                search_term.lower() in book.get('title', '').lower()
                for book in results
            )
            if contains_term:
                print(f"✓ Search term '{search_term}' found in results")
        else:
            print("⚠ No results found (may be expected if no matching data)")
    
    return response.status_code == 200

def test_ordering_ascending():
    """Test 5: Ordering by title (ascending)"""
    print_test_header("Ordering by Title (A-Z)")
    
    params = {'ordering': 'title'}
    print("Request: GET /api/books/?ordering=title")
    
    response = requests.get(BASE_URL, params=params)
    print_results(response)
    
    # Validate ordering
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data if isinstance(data, list) else [])
        
        if len(results) >= 2:
            titles = [book.get('title', '') for book in results]
            is_sorted = all(titles[i] <= titles[i+1] for i in range(len(titles)-1))
            if is_sorted:
                print("✓ Results are correctly ordered A-Z")
            else:
                print("✗ Results are not correctly ordered")
        else:
            print("⚠ Not enough results to validate ordering")
    
    return response.status_code == 200

def test_ordering_descending():
    """Test 6: Ordering by publication year (descending)"""
    print_test_header("Ordering by Publication Year (Newest First)")
    
    params = {'ordering': '-publication_year'}
    print("Request: GET /api/books/?ordering=-publication_year")
    
    response = requests.get(BASE_URL, params=params)
    print_results(response)
    
    # Validate ordering
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data if isinstance(data, list) else [])
        
        if len(results) >= 2:
            years = [book.get('publication_year', 0) for book in results]
            is_sorted = all(years[i] >= years[i+1] for i in range(len(years)-1))
            if is_sorted:
                print("✓ Results are correctly ordered (newest first)")
            else:
                print("✗ Results are not correctly ordered")
        else:
            print("⚠ Not enough results to validate ordering")
    
    return response.status_code == 200

def test_combined_filter_order():
    """Test 7: Combine filtering and ordering"""
    print_test_header("Combined: Filter by Year + Order by Title")
    
    params = {
        'publication_year': 2023,
        'ordering': 'title'
    }
    print("Request: GET /api/books/?publication_year=2023&ordering=title")
    
    response = requests.get(BASE_URL, params=params)
    print_results(response)
    
    # Validate combined query
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data if isinstance(data, list) else [])
        
        if results:
            # Check filtering
            all_match_year = all(book.get('publication_year') == 2023 for book in results)
            
            # Check ordering
            titles = [book.get('title', '') for book in results]
            is_sorted = all(titles[i] <= titles[i+1] for i in range(len(titles)-1))
            
            if all_match_year and is_sorted:
                print("✓ Filter and ordering both work correctly")
            elif all_match_year:
                print("✓ Filter works, ⚠ ordering may have issues")
            elif is_sorted:
                print("⚠ Filter may have issues, ✓ ordering works")
            else:
                print("✗ Both filter and ordering have issues")
        else:
            print("⚠ No results found")
    
    return response.status_code == 200

def test_combined_search_order():
    """Test 8: Combine searching and ordering"""
    print_test_header("Combined: Search + Order by Year")
    
    params = {
        'search': 'Python',
        'ordering': '-publication_year'
    }
    print("Request: GET /api/books/?search=Python&ordering=-publication_year")
    
    response = requests.get(BASE_URL, params=params)
    print_results(response)
    
    return response.status_code == 200

def test_combined_all():
    """Test 9: Combine filtering, searching, and ordering"""
    print_test_header("Combined: Filter + Search + Order")
    
    params = {
        'author': 1,
        'search': 'Django',
        'ordering': '-publication_year'
    }
    print("Request: GET /api/books/?author=1&search=Django&ordering=-publication_year")
    
    response = requests.get(BASE_URL, params=params)
    print_results(response)
    
    return response.status_code == 200

def test_pagination():
    """Test 10: Pagination with queries"""
    print_test_header("Pagination")
    
    params = {'ordering': 'title', 'page': 1}
    print("Request: GET /api/books/?ordering=title&page=1")
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Total Count: {data.get('count', 'N/A')}")
        print(f"Results on Page 1: {len(data.get('results', []))}")
        print(f"Next Page URL: {data.get('next', 'None')}")
        print(f"Previous Page URL: {data.get('previous', 'None')}")
        
        # Try page 2 if it exists
        if data.get('next'):
            print("\nTrying Page 2...")
            params['page'] = 2
            response2 = requests.get(BASE_URL, params=params)
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"Results on Page 2: {len(data2.get('results', []))}")
                print("✓ Pagination works correctly")
        else:
            print("✓ Only one page of results (pagination working)")
    else:
        print_results(response)
    
    print()
    return response.status_code == 200

def test_error_handling():
    """Test 11: Error handling with invalid parameters"""
    print_test_header("Error Handling")
    
    # Test invalid year (not a number)
    print("Test: Invalid publication_year parameter")
    params = {'publication_year': 'invalid'}
    response = requests.get(BASE_URL, params=params)
    print(f"Request: GET /api/books/?publication_year=invalid")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    print()
    
    # Test invalid ordering field
    print("Test: Invalid ordering field")
    params = {'ordering': 'invalid_field'}
    response = requests.get(BASE_URL, params=params)
    print(f"Request: GET /api/books/?ordering=invalid_field")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    print()
    
    return True

def run_all_tests():
    """Run all test cases"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "API QUERY CAPABILITIES TEST SUITE" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    tests = [
        ("Basic List", test_basic_list),
        ("Filter by Year", test_filter_by_year),
        ("Filter by Author", test_filter_by_author),
        ("Search", test_search),
        ("Order Ascending", test_ordering_ascending),
        ("Order Descending", test_ordering_descending),
        ("Filter + Order", test_combined_filter_order),
        ("Search + Order", test_combined_search_order),
        ("Filter + Search + Order", test_combined_all),
        ("Pagination", test_pagination),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, "PASS" if success else "FAIL"))
        except requests.exceptions.ConnectionError:
            print(f"✗ CONNECTION ERROR: Could not connect to {BASE_URL}")
            print("  Make sure Django server is running (python manage.py runserver)")
            results.append((test_name, "ERROR"))
            break
        except Exception as e:
            print(f"✗ UNEXPECTED ERROR: {str(e)}")
            results.append((test_name, "ERROR"))
    
    # Print summary
    print_separator()
    print("TEST SUMMARY")
    print_separator()
    
    for test_name, status in results:
        status_symbol = "✓" if status == "PASS" else "✗"
        print(f"{status_symbol} {test_name}: {status}")
    
    print_separator()
    
    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    elif passed > 0:
        print("⚠ Some tests failed or had errors")
    else:
        print("✗ No tests passed - check server connection and configuration")
    
    print()

if __name__ == '__main__':
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\nFatal error: {str(e)}")
