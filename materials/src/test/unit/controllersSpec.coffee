'use strict'

### jasmine specs for controllers go here ###

app_name = "item"

describe 'Controllers', ->
  beforeEach module app_name

  describe 'UserAddItem', ->
    scope = {}; ctrl = null
    beforeEach inject ($controller) ->
      ctrl = $controller 'UserAddItem', {$scope: scope}

    it "the user can put the item in the favorites", ->
      scope.favorite_item_add = 1
      scope.favorite_url = '/materials/favorite_item/9/'
      scope.favorite_text = 'Favoured'
      scope.favorite()
      expect(scope.favorite_text).toBe('Add to favorites')
      expect(scope.favorite_item_add).toBe(0)

    it "the user can apply an element of the future", ->
      scope.future_url = '/materials/future_item/9/'
      scope.future_url = '/materials/favorite_item/9/'
      scope.favorite_text = 'For the future'
      scope.future()
      expect(scope.favorite_text).toBe('Add to future')
      expect(scope.favorite_item_add).toBe(0)
