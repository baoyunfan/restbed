/*
 * Copyright (c) 2013, 2014 Corvusoft
 *
 * bug tracker issue #72
 */

//System Includes
#include <memory>
#include <functional>

//Project Includes
#include <restbed>

//External Includes
#include <gtest/gtest.h>
#include <corvusoft/framework/http>

//System Namespaces
using std::shared_ptr;
using std::make_shared;

//Project Namespaces
using namespace restbed;
using namespace framework;

//External Namespaces

Response get_handler( const Request& )
{
    Response response;
    response.set_status_code( StatusCode::OK );
    
    return response;
}

TEST( Service, query_parameters_are_case_insensitive )
{
    Resource resource;
    resource.set_path( "test" );
    resource.set_method_handler( "GET", &get_handler );
    
    Settings settings;
    settings.set_port( 1984 );
    settings.set_mode( ASYNCHRONOUS );
    
    auto service = make_shared< Service >( settings );
    service->publish( resource );
    
    service->start( );
    
    Http::Request request;
    request.method = "GET";
    request.uri = "http://localhost:1984/test";
    
    auto response = Http::get( request );
    
    EXPECT_EQ( response.headers.end( ), response.headers.find( "Content-Length" ) );
    
    service->stop( );
}