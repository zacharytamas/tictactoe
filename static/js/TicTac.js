
(function () {

  var TT = window.TicTac = {};

  ////////////////////////////////////////////////
  // Models
  ////////////////////////////////////////////////

  TT.BoardModel = Backbone.Model.extend({
    url: '/game'
  });

  TT.boardModel = new TT.BoardModel();

}());
