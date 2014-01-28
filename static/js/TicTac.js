
(function () {

  var TT = window.TicTac = {};

  ////////////////////////////////////////////////
  // Models
  ////////////////////////////////////////////////

  TT.BoardModel = Backbone.Model.extend({
    url: '/game',

    markSquare: function (square) {
      var state = this.toJSON().board_state;

      if (state[square] !== null) {
        return false;
      }

      state[square] = 'X';
      this.set({board_state: state});

      return true;
    }

  });

  ////////////////////////////////////////////////
  // Views
  ////////////////////////////////////////////////

  TT.BoardView = Backbone.View.extend({
    el: 'body',

    events: {
      'click li': 'squareWasClicked',
      'click .replay-button': 'replay'
    },

    initialize: function () {
      this.listenTo(TT.boardModel, 'change', this.renderUpdates);
    },

    replay: function (event) {
      event.preventDefault();
      TT.boardModel.fetch();
    },

    squareWasClicked: function (event) {
      var $square = $(event.currentTarget);
      var squareSelected = parseInt($square.attr('id').split('-')[1], 10);
      var marked = TT.boardModel.markSquare(squareSelected);

      event.preventDefault();

      if (marked) {
        TT.boardModel.save();
      } else {
        alert('invalid choice');
      }
    },

    render: function () {
      return this.renderUpdates();
    },

    renderUpdates: function () {

      var win = TT.boardModel.get('win');

      if (win && win[0]) {

        // Highlight the squares responsible for the win.
        for (var i = 0; i < 9; i++) {
          if (win[0] === 'TIE') {
            break;
          }

          if ((1 << i) & win[1]) {
            $('#square-' + i).addClass('winning');
          }
        }

      } else {
        this.$('li').removeClass('winning');
      }

      return this.renderSquares();
    },

    renderSquares: function () {
      _.each(TT.boardModel.get('board_state'), function (value, i) {
        var square = $('#square-' + i);
        if (value !== null) {
          square.find('.back').text(value);
          square.addClass('marked');
        } else {
          square.removeClass('marked');
        }
      });

      return this;
    }
  });

  // Setup data
  TT.boardModel = new TT.BoardModel();

  // Setup the interface
  TT.boardView = new TT.BoardView().render();

  // Fetch initial game state.
  TT.boardModel.fetch();

}());
